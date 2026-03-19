# Internationalization & Localization (Compressed)
# ID: i18n
# Module key (for fragment IDs): `internationalization` (see `master_index.yaml.pattern_map`)
# Version: 1.0.0
# Status: active
# Last reviewed: 2026-02-23
# Assumptions: UI/UX governs user interface; this governs locale handling, translation, and cultural adaptation.
# License: CC-BY-4.0
# License URL: https://creativecommons.org/licenses/by/4.0/
# Origin: maintainer
# Adoption Status: adopted
# Standard Inclusion: canonical-reference
# Canonical Manifest Pin: FITPAC 1.0.0 reference distribution

## p1: Locale Contract
```yaml
triggers: []
requires_primitives: [Entity, Authority]
output_type: constraint
domain: i18n
category: other
```

- Primitives: Locale (language, region, script), LocaleIdentifier (BCP47 tag), LocaleResolution.
- Invariants: System MUST determine user locale explicitly (internationalization.inv.1).
- Triggers: locale_unknown, locale_unsupported.
- RULE: Accept locale from: user preference, Accept-Language header, URL, or default. Use BCP47 identifiers (en-US, zh-Hans-CN). Define supported locales. Fallback: requested → language-only → default. Log locale resolution for debugging.

## p2: String Externalization
```yaml
triggers: []
requires_primitives: [Entity, Authority]
output_type: constraint
domain: i18n
category: other
```

- Primitives: MessageKey, MessageBundle (locale, messages), MessageTemplate (key, placeholders).
- Invariants: User-visible strings MUST NOT be hardcoded (internationalization.inv.2).
- Triggers: untranslated_string, hardcoded_text.
- RULE: Extract all user-visible strings to MessageBundle. Use MessageKey for lookup. Support MessageTemplate with placeholders. Enforce via linter/code review. Exception: log messages (typically English-only).

## p3: Translation Workflow
```yaml
triggers: []
requires_primitives: [Entity, Authority]
output_type: constraint
domain: i18n
category: other
```

- Primitives: TranslationRequest (strings, source_locale, target_locales), TranslationStatus, TranslationQuality.
- Triggers: translation_pending, translation_outdated.
- RULE: Define translation workflow: extract strings, send to translators, review, integrate. Track TranslationStatus per locale. Handle: missing translations (fallback), outdated translations (flag). Quality: human review for critical content.

## p4: Plural Forms
```yaml
triggers: []
requires_primitives: [Entity, Authority]
output_type: constraint
domain: i18n
category: other
```

- Primitives: PluralRule (locale, categories), PluralCategory (zero, one, two, few, many, other).
- Invariants: Plural-sensitive messages MUST use locale-appropriate plural rules (internationalization.inv.3).
- Triggers: plural_error, incorrect_plural.
- RULE: Different languages have different plural rules (English: 1 vs other; Arabic: 6 forms). Use CLDR plural rules. Messages like "N items" need plural variants. Test with various counts per locale.

## p5: Date and Time Formatting
```yaml
triggers: []
requires_primitives: [Entity, Authority]
output_type: constraint
domain: i18n
category: other
```

- Primitives: DateTimeFormat (locale, pattern, timezone), CalendarSystem.
- Invariants: Date/time display MUST respect user locale and timezone (internationalization.inv.4).
- Triggers: datetime_format_mismatch, timezone_error.
- RULE: Store dates in UTC. Display in user's timezone and locale format. Support: short, medium, long, full formats. Handle: 12-hour vs 24-hour, date order (MDY vs DMY), calendar systems (Gregorian, Hijri). Use CLDR patterns.

## p6: Number Formatting
```yaml
triggers: []
requires_primitives: [Entity, Authority]
output_type: constraint
domain: i18n
category: other
```

- Primitives: NumberFormat (locale, style, precision), NumberStyle (decimal, percent, currency, scientific).
- Invariants: Number display MUST respect locale conventions (internationalization.inv.5).
- Triggers: number_format_error.
- RULE: Format numbers per locale: decimal separator (. vs ,), grouping (1,000 vs 1.000 vs 1 000). Currency: symbol position, precision. Percent: multiplied by 100. Use standard library formatters.

## p7: Currency Handling
```yaml
triggers: []
requires_primitives: [Entity, Authority]
output_type: constraint
domain: i18n
category: other
```

- Primitives: Currency (code, symbol, precision), CurrencyFormat, ExchangeRate.
- Invariants: Currency amounts MUST display with correct symbol and precision (internationalization.inv.6).
- Triggers: currency_mismatch, precision_error.
- RULE: Store currency with ISO 4217 code. Display with localized symbol ($ vs USD vs US$). Respect precision (USD: 2, JPY: 0, BTC: 8). Exchange rates: source, timestamp, calculation rules. Handle multi-currency scenarios.

## p8: Text Direction
```yaml
triggers: []
requires_primitives: [Entity, Authority]
output_type: constraint
domain: i18n
category: other
```

- Primitives: TextDirection (LTR, RTL, auto), BidiText.
- Triggers: bidi_error, layout_broken.
- RULE: Support RTL languages (Arabic, Hebrew). Mark text direction explicitly. Handle bidirectional text (mixed LTR/RTL). Test UI layout in RTL mode. CSS: use logical properties (start/end vs left/right).

## p9: Content Localization
```yaml
triggers: []
requires_primitives: [Entity, Authority]
output_type: constraint
domain: i18n
category: other
```

- Primitives: LocalizedContent (type: text, image, video, document), ContentVariant.
- Triggers: content_not_localized.
- RULE: Beyond text: images with text, videos with subtitles, documents, legal content. Define which content requires localization. Manage ContentVariants per locale. Fallback to source locale if variant unavailable.

## p10: Locale-Aware Validation
```yaml
triggers: []
requires_primitives: [Entity, Authority]
output_type: constraint
domain: i18n
category: other
```

- Primitives: ValidationRule (locale_dependent), LocalizedValidation.
- Triggers: validation_locale_error.
- RULE: Some validations are locale-dependent: postal codes, phone numbers, addresses, names. Use locale-aware validators. Accept various input formats. Normalize for storage. Display in locale format.

## p11: Sorting and Collation
```yaml
triggers: []
requires_primitives: [Entity, Authority]
output_type: constraint
domain: i18n
category: other
```

- Primitives: Collation (locale, strength, case_sensitivity), SortOrder.
- Invariants: String sorting MUST use locale-appropriate collation (internationalization.inv.7).
- Triggers: sort_order_unexpected.
- RULE: Different locales sort differently (ä: end in English, after a in Swedish). Use locale-aware collation. Configure: case sensitivity, accent sensitivity. Test sorting with locale-specific characters.

## p12: Locale Testing
```yaml
triggers: []
requires_primitives: [Entity, Authority]
output_type: constraint
domain: i18n
category: other
```

- Primitives: PseudoLocalization, LocaleTestSuite.
- Triggers: i18n_test_failed.
- RULE: Test i18n early with PseudoLocalization (expand strings, add accents). Test: string expansion (German +30%), RTL layout, plural forms, date/number formats. Include i18n checks in LocaleTestSuite. Test with actual translators for critical markets.
