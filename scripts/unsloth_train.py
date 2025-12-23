#!/usr/bin/env python3
"""
Unsloth LoRA fine-tune for LuminAI Genesis.

Trains a base model (llama3.2 or similar) on persona-aligned SFT data.
Outputs LoRA weights compatible with Ollama serving via Modelfile.

Usage:
    source ../unsloth-venv/bin/activate
    python scripts/unsloth_train.py \
        --model_name "unsloth/llama-3-8b-bnb-4bit" \
        --output_dir "models/luminai-lora" \
        --num_epochs 3 \
        --batch_size 4
"""

import argparse
import json
import logging
from pathlib import Path

from datasets import Dataset
from transformers import TrainingArguments
from trl import SFTTrainer
from unsloth import FastLanguageModel, is_bfloat16_supported


def load_training_data(data_path: str) -> Dataset:
    """Load JSONL training data and convert to HuggingFace Dataset."""

    texts = []
    with Path(data_path).open(encoding="utf-8") as f:
        for line in f:
            item = json.loads(line)
            texts.append(item["text"])

    return Dataset.from_dict({"text": texts})


def setup_model_and_tokenizer(
    model_name: str,
    max_seq_length: int = 2048,
    load_in_4bit: bool = True,
):
    """Initialize Unsloth FastLanguageModel with LoRA config."""
    model, tokenizer = FastLanguageModel.from_pretrained(
        model_name=model_name,
        max_seq_length=max_seq_length,
        dtype=None,  # Auto-detect
        load_in_4bit=load_in_4bit,
    )

    # Apply LoRA
    model = FastLanguageModel.get_peft_model(
        model,
        r=16,  # LoRA rank
        lora_alpha=16,
        lora_dropout=0.05,
        bias="none",
        use_gradient_checkpointing="unsloth",
        random_state=42,
        use_rslora=False,  # rank-stabilized LoRA
        target_modules=["q_proj", "k_proj", "v_proj", "o_proj"],
    )

    return model, tokenizer


def train(
    model_name: str = "unsloth/llama-3-8b-bnb-4bit",
    data_path: str = "data/training/persona_sft_dataset_complete.jsonl",
    output_dir: str = "models/luminai-lora",
    num_epochs: int = 3,
    batch_size: int = 2,
    learning_rate: float = 2e-4,
    max_seq_length: int = 1024,
    use_cpu: bool = False,
):
    """Fine-tune model using Unsloth with LuminAI persona-aligned data."""

    logger = logging.getLogger(__name__)
    logging.basicConfig(level=logging.INFO, format="%(message)s")

    logger.info("%s", "=" * 70)
    logger.info("UNSLOTH FINE-TUNE: LuminAI Genesis")
    logger.info("%s", "=" * 70)
    logger.info("Model: %s", model_name)
    logger.info("Data: %s", data_path)
    logger.info("Output: %s", output_dir)
    logger.info("Epochs: %d, Batch Size: %d", num_epochs, batch_size)
    logger.info("%s", "=" * 70)

    # Load data
    logger.info("[1/5] Loading training data...")
    train_dataset = load_training_data(data_path)
    logger.info("  ✓ Loaded %d examples", len(train_dataset))

    # Setup model and tokenizer
    logger.info("[2/5] Initializing Unsloth model with LoRA...")
    model, tokenizer = setup_model_and_tokenizer(
        model_name,
        max_seq_length=max_seq_length,
    )
    logger.info("  ✓ Model loaded in 4-bit quantization")
    logger.info("  ✓ LoRA applied (rank=16, alpha=16)")
    # Training arguments
    logger.info("[3/5] Configuring training arguments...")

    # CPU mode adjustments
    if use_cpu:
        logger.warning("CPU-only mode enabled (no CUDA available)")
        logger.warning("Training will be significantly slower")
        batch_size = min(batch_size, 1)  # Reduce to 1 for CPU
    training_args = TrainingArguments(
        output_dir=output_dir,
        per_device_train_batch_size=batch_size,
        gradient_accumulation_steps=4 if use_cpu else 2,  # More accumulation on CPU
        warmup_steps=5 if use_cpu else 10,
        num_train_epochs=num_epochs,
        learning_rate=learning_rate,
        fp16=False if use_cpu else (not is_bfloat16_supported()),
        bf16=False if use_cpu else is_bfloat16_supported(),
        logging_steps=2 if use_cpu else 5,
        save_steps=50 if use_cpu else 25,
        save_total_limit=2,
        seed=42,
        optim="adamw_torch" if use_cpu else "paged_adamw_8bit",
        weight_decay=0.01,
        max_grad_norm=1.0,
        no_cuda=use_cpu,
    )
    logger.info("  ✓ Learning rate: %s", learning_rate)
    logger.info("  ✓ Gradient accumulation: %d steps", (4 if use_cpu else 2))
    logger.info("  ✓ Batch size: %d", batch_size)
    if not use_cpu:
        logger.info(
            "  ✓ Using %s", ("bfloat16" if is_bfloat16_supported() else "float16"),
        )

    # Create trainer
    logger.info("[4/5] Initializing SFT trainer...")
    trainer = SFTTrainer(
        model=model,
        tokenizer=tokenizer,
        train_dataset=train_dataset,
        dataset_text_field="text",
        max_seq_length=max_seq_length,
        args=training_args,
        packing=True,  # Pack multiple examples into one sequence
    )
    logger.info("  ✓ Trainer ready (packing enabled)")

    # Train
    logger.info("[5/5] Starting training...")
    logger.info("%s", "-" * 70)
    trainer.train()
    logger.info("%s", "-" * 70)
    logger.info("  ✓ Training complete!")

    # Save
    logger.info("[SAVE] Saving LoRA weights...")
    model.save_pretrained(output_dir)
    tokenizer.save_pretrained(output_dir)
    logger.info("  ✓ LoRA weights saved to: %s", output_dir)
    # Merge to full weights (optional, for GGUF conversion)
    logger.info("[MERGE] Creating merged model (for GGUF conversion)...")
    merged_output = f"{output_dir}_merged"
    model = model.merge_and_unload()
    model.save_pretrained(merged_output)
    tokenizer.save_pretrained(merged_output)
    logger.info("  ✓ Merged weights saved to: %s", merged_output)

    logger.info("%s", "=" * 70)
    logger.info("TRAINING COMPLETE")
    logger.info("%s", "=" * 70)
    logger.info("Next steps:")
    logger.info("1. Convert merged weights to GGUF:")
    logger.info("   cd %s", merged_output)
    logger.info("   python -m llama_cpp.llama_quantize model.safetensors model.gguf")
    logger.info("2. Create Ollama model:")
    logger.info("   ollama create luminai-unsloth -f Modelfile")
    logger.info("3. Test in API:")
    logger.info("   curl -X POST http://localhost:8000/api/chat \\")
    logger.info("     -H 'Content-Type: application/json' \\")
    logger.info(
        "     -d %s",
        '{"session_id": "test", "message": "Hello", "model": "luminai-unsloth"}',
    )
    logger.info("%s", "=" * 70)


if __name__ == "__main__":
    parser = argparse.ArgumentParser(
        description="Unsloth fine-tune for LuminAI Genesis",
    )
    parser.add_argument(
        "--model_name",
        type=str,
        default="unsloth/llama-3-8b-bnb-4bit",
        help="HuggingFace model ID to fine-tune",
    )
    parser.add_argument(
        "--data_path",
        type=str,
        default="data/training/persona_sft_dataset_complete.jsonl",
        help="Path to JSONL training data",
    )
    parser.add_argument(
        "--output_dir",
        type=str,
        default="models/luminai-lora",
        help="Output directory for LoRA weights",
    )
    parser.add_argument(
        "--num_epochs",
        type=int,
        default=3,
        help="Number of training epochs",
    )
    parser.add_argument(
        "--batch_size",
        type=int,
        default=2,
        help="Training batch size per device",
    )
    parser.add_argument(
        "--learning_rate",
        type=float,
        default=2e-4,
        help="Learning rate",
    )
    parser.add_argument(
        "--max_seq_length",
        type=int,
        default=1024,
        help="Maximum sequence length",
    )
    parser.add_argument(
        "--use_cpu",
        action="store_true",
        help="Force CPU-only training (no CUDA)",
    )

    args = parser.parse_args()

    train(
        model_name=args.model_name,
        data_path=args.data_path,
        output_dir=args.output_dir,
        num_epochs=args.num_epochs,
        batch_size=args.batch_size,
        learning_rate=args.learning_rate,
        max_seq_length=args.max_seq_length,
        use_cpu=args.use_cpu,
    )
