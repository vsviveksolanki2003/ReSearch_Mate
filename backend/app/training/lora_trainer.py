"""LoRA / QLoRA fine-tuning configuration and runner for Llama 3.1."""
from dataclasses import dataclass, field
from typing import List, Dict, Any

@dataclass
class LoRATrainingConfig:
    base_model: str = "meta-llama/Meta-Llama-3.1-8B-Instruct"
    output_dir: str = "./models/lora_adapter"
    lora_r: int = 16
    lora_alpha: int = 32
    lora_dropout: float = 0.05
    target_modules: List[str] = field(default_factory=lambda: ["q_proj", "v_proj", "k_proj", "o_proj"])
    learning_rate: float = 2e-4
    num_train_epochs: int = 3
    per_device_train_batch_size: int = 2
    gradient_accumulation_steps: int = 4
    optim: str = "paged_adamw_8bit"
    lr_scheduler_type: str = "cosine"
    max_seq_length: int = 2048

def get_peft_configuration(config: LoRATrainingConfig) -> Dict[str, Any]:
    """Return PEFT LoraConfig dictionary."""
    return {
        "r": config.lora_r,
        "lora_alpha": config.lora_alpha,
        "lora_dropout": config.lora_dropout,
        "target_modules": config.target_modules,
        "bias": "none",
        "task_type": "CAUSAL_LM"
    }

def get_training_arguments(config: LoRATrainingConfig) -> Dict[str, Any]:
    """Return HuggingFace TrainingArguments dictionary."""
    return {
        "output_dir": config.output_dir,
        "learning_rate": config.learning_rate,
        "num_train_epochs": config.num_train_epochs,
        "per_device_train_batch_size": config.per_device_train_batch_size,
        "gradient_accumulation_steps": config.gradient_accumulation_steps,
        "optim": config.optim,
        "lr_scheduler_type": config.lr_scheduler_type,
        "max_seq_length": config.max_seq_length,
        "fp16": False,
        "bf16": True,
        "logging_steps": 10,
        "save_strategy": "epoch"
    }
