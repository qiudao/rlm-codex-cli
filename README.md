# rlm-codex-cli

[GitHub: qiudao/rlm-codex-cli](https://github.com/qiudao/rlm-codex-cli)

`rlm-codex` is a small local CLI for long-context questions. It reads a file or
directory, chunks the context locally, and delegates each reasoning step to
`codex exec`, so usage follows your current Codex CLI login and quota path.

It is intentionally simple:

- no OpenAI API key is used by this tool
- no third-party Python dependencies are required
- file and directory context are supported
- PDF is supported when `pdftotext` is installed
- large contexts use a map/reduce flow over multiple `codex exec` calls

## Why

Codex CLI is good at engineering tasks, but sometimes you want to ask questions
over a context that is too large to paste into one prompt: a PDF, a long log, or
a whole source tree. This tool acts as a thin long-context preprocessor:

1. read local context
2. split it into chunks
3. ask Codex to analyze each chunk
4. ask Codex to synthesize the partial answers

It is inspired by Recursive Language Model style workflows, but stays pragmatic:
the recursion happens at the CLI layer through repeated `codex exec` calls.

## Background

This project was created after reading the Recursive Language Models paper and
the accompanying minimal implementation:

- Paper: [Recursive Language Models](https://arxiv.org/abs/2512.24601)
- Paper PDF: [arXiv PDF](https://arxiv.org/pdf/2512.24601)
- Original RLM codebase: [alexzhang13/rlm](https://github.com/alexzhang13/rlm)
- Minimal reference project: [alexzhang13/rlm-minimal](https://github.com/alexzhang13/rlm-minimal)

The original RLM idea is to place long context in an external environment, let a
root model inspect and transform that context through code, and recursively call
sub-models over smaller pieces. The minimal project demonstrates that pattern
with a Python REPL and OpenAI API calls.

This repository adapts the idea for a different local workflow: instead of
building another OpenAI API client, it uses the already-installed Codex CLI as
the reasoning backend. The reason is practical: Codex already has local project
awareness, a non-interactive `codex exec` mode, sandbox flags, and an existing
login/quota path. `rlm-codex` keeps only the long-context orchestration layer:
collect files, split context, ask Codex for partial answers, then synthesize.

## Requirements

- Python 3.9+
- [Codex CLI](https://developers.openai.com/codex/cli) available as `codex`
- A working Codex CLI login, usually checked with:

```bash
codex doctor
```

For PDF input, install `pdftotext`:

```bash
brew install poppler
```

Check it with:

```bash
which pdftotext
```

## Usage And Quota

This tool does not call the OpenAI API directly. It shells out to `codex exec`.
That means model usage follows the active Codex CLI authentication and Codex
usage path on your machine.

In practical terms:

- `./bin/rlm-codex ...` -> `codex exec ...`
- no `OPENAI_API_KEY` is read by this project
- if your Codex CLI is logged in with a ChatGPT plan, usage follows that Codex
  plan path
- if your Codex CLI is configured differently, usage follows that configuration

Use `--dry-run` to inspect chunking without invoking Codex.

## Quick Start

Clone and run:

```bash
git clone https://github.com/qiudao/rlm-codex-cli.git
cd rlm-codex-cli
./bin/rlm-codex --help
```

From this directory:

```bash
./bin/rlm-codex --help
```

Optional editable install:

```bash
python3 -m pip install -e .
rlm-codex --help
```

## Usage

Ask a question about a file:

```bash
./bin/rlm-codex query --context ~/work/rlm-minimal/README.md --query "总结这个项目"
```

Ask a question about a directory:

```bash
./bin/rlm-codex query --context /Users/k/opensrc/AI/rlm-minimal --query "解释项目架构"
```

Analyze a PDF if `pdftotext` exists:

```bash
./bin/rlm-codex query --context /Users/k/opensrc/AI/rlm-minimal/2512.24601.pdf --query "总结论文原理"
```

Preview chunking without calling Codex:

```bash
./bin/rlm-codex query --context . --query "what is this?" --dry-run
```

Use a specific Codex model:

```bash
./bin/rlm-codex query \
  --context ./some-repo \
  --query "找出主要模块和风险" \
  --chunk-chars 100000 \
  --max-chunks 12 \
  --model gpt-5-codex
```

Use a working directory for Codex:

```bash
./bin/rlm-codex query \
  --context ./src \
  --query "find likely bugs" \
  --cwd .
```

Enable Codex web search:

```bash
./bin/rlm-codex query \
  --context ./paper.md \
  --query "compare this with current docs" \
  --search
```

## Options

```text
--context, -c        File or directory to read
--query, -q          Question to answer
--chunk-chars        Approximate characters per chunk, default 100000
--max-chunks         Maximum chunks sent to Codex, default 10
--max-file-chars     Maximum characters read from one file, default 300000
--exclude            Additional file or directory name to exclude
--model, -m          Codex model override
--cwd                Working directory for codex exec
--search             Enable Codex web search
--timeout            Seconds before a codex exec call times out
--dry-run            Show chunk stats without calling Codex
```

## Safety Model

Local context is treated as untrusted text in prompts. The generated Codex tasks
are analysis-only and pass:

```bash
codex exec --sandbox read-only --skip-git-repo-check --ephemeral
```

The prompt also tells Codex not to modify files or run commands. The CLI itself
only reads local files and creates temporary files for Codex output capture.

## Limitations

- It is not a secure sandbox for malicious documents.
- Binary files are skipped.
- PDF support depends on `pdftotext`.
- Very large inputs are truncated by `--max-file-chars` and `--max-chunks`.
- Multi-chunk answers are only as good as the partial evidence preserved during
  synthesis.

## Notes

The project intentionally keeps implementation small and dependency-free. The
main code lives in `src/rlm_codex_cli/cli.py`, and `bin/rlm-codex` is a wrapper
that runs it without requiring installation.
