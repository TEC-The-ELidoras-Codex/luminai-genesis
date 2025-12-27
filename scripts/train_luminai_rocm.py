"""
Fine-tune LuminAI Genesis on AMD RX 580 with ROCm.
Pure Transformers + PEFT approach (no Unsloth dependency).

Usage:
    source unsloth-venv/bin/activate
    python scripts/train_luminai_rocm.py
"""

import json
import logging
import os
from pathlib import Path

from datasets import Dataset

os.environ["CUDA_VISIBLE_DEVICES"] = ""  # Force CPU only

logger = logging.getLogger(__name__)


# Heavy ML imports are done inside `main()` to keep top-level imports clean
# and avoid flake8 E402 (module-level import not at top of file) when we
# need to perform environment configuration before model initialization.


def load_jsonl_dataset(path: str) -> Dataset:
    """Load JSONL training data."""
    texts = []
    with Path(path).open(encoding="utf-8") as f:
        for line in f:
            if line.strip():
                try:
                    item = json.loads(line)
                    texts.append(item["text"])
                except json.JSONDecodeError:
                    continue

    return Dataset.from_dict({"text": texts})


def tokenize_function(examples, tokenizer, max_length=1024):
    """Tokenize text examples."""
    return tokenizer(
        examples["text"],
        truncation=True,
        max_length=max_length,
        padding="max_length",
    )


def main():
    # Configure lightweight CLI logging for scripts
    logging.basicConfig(level=logging.INFO, format="%(message)s")
    logger.info("%s", "=" * 70)
    logger.info("LuminAI Genesis Fine-Tuning: AMD RX 580 + ROCm")
    logger.info("%s", "=" * 70)

    # Config
    model_name = (
        "TinyLlama/TinyLlama-1.1B-Chat-v1.0"  # Only 2.2GB, fully open, good for testing
    )
    data_path = "data/training/persona_sft_dataset_clean.jsonl"
    output_dir = "models/luminai-genesis-v1"

    # Import heavy ML libraries here so environment variables (if any)
    # can be configured before model libraries initialize.
    import torch

    logger.info("Model: %s", model_name)
    logger.info("Data: %s", data_path)
    logger.info("Output: %s", output_dir)
    logger.info(
        "Device: %s",
        (torch.cuda.get_device_name(0) if torch.cuda.is_available() else "CPU"),
    )
    logger.info("%s", "=" * 70)

    from peft import LoraConfig, get_peft_model
    from transformers import (
        AutoModelForCausalLM,
        AutoTokenizer,
        DataCollatorForLanguageModeling,
        Trainer,
        TrainingArguments,
    )

    # Load tokenizer
    logger.info("[1/6] Loading tokenizer...")
    tokenizer = AutoTokenizer.from_pretrained(model_name)
    tokenizer.pad_token = tokenizer.eos_token
    tokenizer.padding_side = "right"
    logger.info("  ✓ Tokenizer ready")

    # Load base model (FP32 for RX 580 gfx803 compatibility)
    logger.info("[2/6] Loading base model...")
    model = AutoModelForCausalLM.from_pretrained(
        model_name,
        torch_dtype=torch.float32,
        device_map="cpu",  # CPU first, will move to GPU after LoRA applied
        trust_remote_code=True,
    )
    logger.info("  ✓ Model loaded on: CPU (will move to GPU after LoRA)")

    # Prepare for LoRA (skip kbit prep for RX 580 compatibility)
    logger.info("[3/6] Applying LoRA configuration...")

    lora_config = LoraConfig(
        r=16,
        lora_alpha=16,
        target_modules=["q_proj", "k_proj", "v_proj", "o_proj"],
        lora_dropout=0.05,
        bias="none",
        task_type="CAUSAL_LM",
    )

    model = get_peft_model(model, lora_config)
    model.print_trainable_parameters()
    logger.info("  ✓ LoRA applied (r=16, alpha=16)")

    # Keep on CPU for now (RX 580 HIP compatibility issues)
    logger.warning("Training on CPU (RX 580 has HIP kernel compatibility issues)")

    # Load and tokenize dataset
    logger.info("[4/6] Loading training data...")
    dataset = load_jsonl_dataset(data_path)
    logger.info("  ✓ Loaded %d examples", len(dataset))

    logger.info("[5/6] Tokenizing dataset...")
    tokenized_dataset = dataset.map(
        lambda x: tokenize_function(x, tokenizer, max_length=1024),
        batched=True,
        remove_columns=dataset.column_names,
    )
    logger.info("  ✓ Tokenization complete")

    # Training arguments
    logger.info("[6/6] Configuring training...")
    training_args = TrainingArguments(
        output_dir=output_dir,
        num_train_epochs=3,
        per_device_train_batch_size=1,  # Small batch for RX 580
        gradient_accumulation_steps=4,
        learning_rate=2e-4,
        fp16=False,  # Use FP32 for RX 580 (gfx803) compatibility
        logging_steps=5,
        save_steps=25,
        save_total_limit=2,
        warmup_steps=10,
        optim="adamw_torch",
        report_to="none",
        remove_unused_columns=False,
    )

    # Data collator
    data_collator = DataCollatorForLanguageModeling(
        tokenizer=tokenizer,
        mlm=False,
    )

    # Trainer
    trainer = Trainer(
        model=model,
        args=training_args,
        train_dataset=tokenized_dataset,
        data_collator=data_collator,
    )

    logger.info("  ✓ Trainer ready")
    logger.info("%s", "=" * 70)
    logger.info("TRAINING START: Witness Protocol (W) Integration")
    logger.info("%s", "=" * 70)

    # Train
    trainer.train()

    logger.info("%s", "=" * 70)
    logger.info("TRAINING COMPLETE")
    logger.info("%s", "=" * 70)

    # Save
    logger.info("Saving model...")
    model.save_pretrained(output_dir)
    tokenizer.save_pretrained(output_dir)
    logger.info("  ✓ Saved to: %s", output_dir)

    logger.info("Next Steps:")
    logger.info("1. Convert to GGUF for Ollama")
    logger.info("2. Create Ollama model: ollama create luminai-genesis")
    logger.info("3. Test in Web UI: http://localhost:8080")
    logger.info("%s", "=" * 70)


if __name__ == "__main__":
    main()
