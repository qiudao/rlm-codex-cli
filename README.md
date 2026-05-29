# rlm-codex-cli

`rlm-codex` is a small local CLI for long-context questions. It reads a file or
directory, chunks the context locally, and delegates each reasoning step to
`codex exec`, so usage follows your current Codex CLI login and quota path.

It is intentionally simple:

- no OpenAI API key is used by this tool
- no third-party Python dependencies are required
- file and directory context are supported
- PDF is supported when `pdftotext` is installed
- large contexts use a map/reduce flow over multiple `codex exec` calls

## Run

From this directory:

```bash
./bin/rlm-codex --help
```

Optional editable install, if your Python environment supports it:

```bash
python3 -m pip install -e .
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

Useful options:

```bash
./bin/rlm-codex query \
  --context ./some-repo \
  --query "找出主要模块和风险" \
  --chunk-chars 100000 \
  --max-chunks 12 \
  --model gpt-5-codex
```

## Notes

Context is treated as untrusted text in prompts. The generated Codex tasks are
analysis-only and pass `--sandbox read-only`, `--skip-git-repo-check`, and
`--ephemeral`.
