# Public Source Tool Audit And Completion

Date: 2026-09-08. Scope: this quant-data-index Skill and its copy in the quant-learning-project repository. The repositories remain separate; this work does not initialize accounts, change trading settings, or send orders.

## User Requirements To Read Before Continuing

The relevant original instructions are:

- "帮我检查一下我的公有仓库里有没有 API。如果没有 API 就行；如果有，就把 API 去除"
- Clarification: "这是我个人的一些密钥啊，URL什么的"
- Final choice: "只删除真实密钥/凭据，保留公开 API URL（推荐）"
- "同样，你对他们进行一下审计和相关的完成工作，然后完成以后直接上传就行"
- "记得分仓库"
- "URL直接保留" and "允许修改D盘F盘"
- "对于他们技术原理涉及的一些应用技术，包括前端的 CSS，以及各种爬虫的相关技术，给我一个大致的方向，然后我去具体地了解"

Interpretation: retain public endpoint documentation, remove real credentials if present, complete the documented unfinished tools, verify them, and publish each project in its own repository. A public API URL identifies a service; a credential grants access and must not be published. This task never reads local private configuration or account credentials.

## Plan And Acceptance

- [x] Read README, SKILL and references before implementation.
- [x] Replace both placeholder scripts using Python standard-library functionality.
- [x] Keep the documented `probe_sources.py --group crypto` and `--all` commands working.
- [x] Make sample source and destination explicit; do not overwrite files.
- [x] Validate HTTP status, payload shape, financial values, units and search results.
- [x] Add offline tests for success and failure boundaries.
- [x] Run actual public-source probes and sample downloads.
- [x] Synchronize the second Skill copy and run its full test suite.
- [ ] Final repository scan, commit and separate upload by the publishing task.

## Bugs And Resolutions

| Issue | Impact | Resolution |
|---|---|---|
| Both Python entry points contained only `# placeholder` | Documented commands performed no useful work | Implemented five public source samples, validated probes and explicit file output |
| Historical availability labels were presented as current guarantees | Users could trust obsolete access or quota claims | Marked the labels as historical, explained current-response checks, removed blanket anonymous-access claims for OpenAlex |
| The Skill referred to login-helper files absent from both repositories | Following instructions led to missing files | Replaced the unavailable file references with a clearly optional browser-login approach |
| `output/` was not ignored in the standalone repository | Generated search/sample results could enter version control | Added `output/` to `.gitignore` |
| Different markets report volume in different units | Users could treat contract counts as BTC | Preserve explicit USDT, contracts and BTC units in normalized records |

All identified implementation bugs in this scope are resolved. Broader credential/history scanning and publishing are owned by the parent repository-audit task.

## Verification

Commands run from the standalone repository root:

```powershell
python -m unittest discover -s tests -v
python scripts/probe_sources.py --all --timeout 10
python scripts/fetch_examples.py --source gate-futures --limit 5 --output output/verified-gate-futures-20260908.json
python scripts/fetch_examples.py --source arxiv --query "quantitative trading" --limit 3 --output output/verified-arxiv-20260908.json
python scripts/fetch_examples.py --source crossref --query "quantitative trading" --limit 3 --output output/verified-crossref-20260908.json
git diff --check
```

Results: 28 offline tests passed in each Skill copy. Live probing at 2026-09-08 00:42 UTC validated all five sources: Gate spot, Gate futures, Binance spot, arXiv and Crossref. Real downloads saved 5 Gate futures candles, 3 arXiv papers and 3 Crossref records. Generated samples stay in the ignored `output/` directory. The diff whitespace check passed; Git reported only its existing LF-to-CRLF conversion notices. After review, explicit truncated-response handling and UTF-8-only XML validation were covered by the final test run.

The tests cover invalid command arguments, missing explicit destination/source, existing-file protection, network failures, HTTP errors, response size/empty-body limits, invalid JSON/XML, XML entities, cross-host or insecure redirects, API business errors, invalid/nonfinite prices, OHLC consistency, timestamp bounds, duplicate bars, exact decimal strings, volume units, normal empty searches, and continuation after one failed source.

## Remaining Limits And Next Work

- Live results are an observation from this machine at the recorded time. They do not prove that a source works in every region or will remain available.
- `--all` covers the five implemented samples, not every link in the reference catalog. Sources needing keys, cookies, paid access or additional adapters are still references only.
- This is a small-sample tool, not a historical backfill service, complete crawler platform or trading system. Daily bars may include the unfinished current day; contract multipliers and historical pagination are not implemented.
- A request timeout bounds each network operation, not the total duration of all sources. Response bodies are capped at 2 MiB. There are no automatic retries; users should observe provider limits before running another batch.
- No front-end or CSS is used by these scripts. Their relevant learning sequence is: Python command-line arguments; HTTP/HTTPS requests; JSON and Atom/XML parsing; numerical validation; safe file output; automated tests. Browser automation and CSS become relevant only when building a browser-based interface or reading pages without a suitable API.
- If future work adds a source, record its public URL, payload format, authentication needs, units, rate rules, empty-result behavior and tests before adding it to `--all`.
