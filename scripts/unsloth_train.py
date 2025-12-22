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

from datasets import Dataset
from transformers import TrainingArguments
from trl import SFTTrainer
from unsloth import FastLanguageModel, is_bfloat16_supported


def load_training_data(data_path: str) -> Dataset:
    """Load JSONL training data and convert to HuggingFace Dataset."""
    texts = []
    with open(data_path) as f:
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

    print("\n" + "=" * 70)
    print("UNSLOTH FINE-TUNE: LuminAI Genesis")
    print("=" * 70)
    print(f"Model: {model_name}")
    print(f"Data: {data_path}")
    print(f"Output: {output_dir}")
    print(f"Epochs: {num_epochs}, Batch Size: {batch_size}")
    print("=" * 70 + "\n")

    # Load data
    print("[1/5] Loading training data...")
    train_dataset = load_training_data(data_path)
    print(f"  ✓ Loaded {len(train_dataset)} examples")

    # Setup model and tokenizer
    print("\n[2/5] Initializing Unsloth model with LoRA...")
    model, tokenizer = setup_model_and_tokenizer(
        model_name,
        max_seq_length=max_seq_length,
    )
    print("  ✓ Model loaded in 4-bit quantization")
    print("  ✓ LoRA applied (rank=16, alpha=16)")

    # Training arguments
    print("\n[3/5] Configuring training arguments...")

    # CPU mode adjustments
    if use_cpu:
        print("  ⚠️  CPU-only mode enabled (no CUDA available)")
        print("  ⚠️  Training will be significantly slower")
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
    print(f"  ✓ Learning rate: {learning_rate}")
    print(f"  ✓ Gradient accumulation: {4 if use_cpu else 2} steps")
    print(f"  ✓ Batch size: {batch_size}")
    if not use_cpu:
        print(f"  ✓ Using {'bfloat16' if is_bfloat16_supported() else 'float16'}")

    # Create trainer
    print("\n[4/5] Initializing SFT trainer...")
    trainer = SFTTrainer(
        model=model,
        tokenizer=tokenizer,
        train_dataset=train_dataset,
        dataset_text_field="text",
        max_seq_length=max_seq_length,
        args=training_args,
        packing=True,  # Pack multiple examples into one sequence
    )
    print("  ✓ Trainer ready (packing enabled)")

    # Train
    print("\n[5/5] Starting training...")
    print("-" * 70)
    trainer.train()
    print("-" * 70)
    print("  ✓ Training complete!")

    # Save
    print("\n[SAVE] Saving LoRA weights...")
    model.save_pretrained(output_dir)
    tokenizer.save_pretrained(output_dir)
    print(f"  ✓ LoRA weights saved to: {output_dir}")

    # Merge to full weights (optional, for GGUF conversion)
    print("\n[MERGE] Creating merged model (for GGUF conversion)...")
    merged_output = f"{output_dir}_merged"
    model = model.merge_and_unload()
    model.save_pretrained(merged_output)
    tokenizer.save_pretrained(merged_output)
    print(f"  ✓ Merged weights saved to: {merged_output}")

    print("\n" + "=" * 70)
    print("TRAINING COMPLETE")
    print("=" * 70)
    print("\nNext steps:")
    print("1. Convert merged weights to GGUF:")
    print(f"   cd {merged_output}")
    print("   python -m llama_cpp.llama_quantize model.safetensors model.gguf")
    print("\n2. Create Ollama model:")
    print("   ollama create luminai-unsloth -f Modelfile")
    print("\n3. Test in API:")
    print("   curl -X POST http://localhost:8000/api/chat \\")
    print("     -H 'Content-Type: application/json' \\")
    print(
        '     -d \'{"session_id": "test", "message": "Hello", "model": "luminai-unsloth"}\'',
    )
    print("=" * 70 + "\n")


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
