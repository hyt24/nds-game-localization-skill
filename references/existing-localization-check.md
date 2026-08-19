# Existing Localization Check

Before reverse engineering or translating, determine whether the exact game already has a localization or an active project. This prevents duplicated work and helps preserve prior community knowledge.

## Identify the exact release

Collect before searching:

- Japanese and romanized title, alternative titles, and series name;
- platform, region, language, publisher, and release year;
- NDS game code from the header;
- ROM revision/version and source SHA-256 when available;
- desired target language and script variant.

A patch for another region or revision may not apply even when the title is identical.

## Search responsibly

Search the open web, GitHub/GitLab, ROM-hacking and fan-translation communities, project blogs, video descriptions, patch databases, and relevant language communities. Search combinations of the title with terms such as `translation`, `localization`, `English patch`, `Chinese patch`, `汉化`, `汉化版`, `补丁`, `NDS`, game code, and target language.

Look for:

- released patches and their supported source hashes;
- source repositories and licenses;
- active or dormant projects;
- partial translations, tools, tables, fonts, and format documentation;
- known bugs, compatibility notes, credits, and contact information.

Do not download or redistribute ROMs. Prefer project pages, source repositories, patch files, checksums, and author statements.

## Ask before proceeding

If anything relevant is found, summarize it with links, date/status, language, supported revision, license or permission status, and known completeness. Then ask the user to choose:

1. use the existing localization as-is;
2. audit or improve it;
3. continue/fork it after confirming permission and license compatibility;
4. create a clean-room localization from the legally obtained source ROM;
5. stop because the existing work already satisfies the goal.

Do not begin extraction, translation, or code reuse until this decision is explicit. If no existing localization is found, say that the search is not proof of absence and continue with the source-ROM audit only after user confirmation.

## Record provenance

Add all findings and the user’s decision to the project manifest and progress log. Keep prior authors’ credits. Never copy text, code, fonts, or artwork from an existing project without compatible licensing or permission.
