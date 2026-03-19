# Accessibility (Compressed)
# ID: a11y
# Module key (for fragment IDs): `accessibility` (see `master_index.yaml.pattern_map`)
# Version: 1.0.0
# Status: active
# Last reviewed: 2026-02-23
# Assumptions: UI/UX governs interface design; this governs accessibility compliance and inclusive design.
# License: CC-BY-4.0
# License URL: https://creativecommons.org/licenses/by/4.0/
# Origin: maintainer
# Adoption Status: adopted
# Standard Inclusion: canonical-reference
# Canonical Manifest Pin: FITPAC 1.0.0 reference distribution

## p1: Compliance Level Contract
```yaml
triggers: [compliance_violation, accessibility_regression]
requires_primitives: [Entity, Authority]
output_type: constraint
domain: a11y
category: other
```

- Primitives: WCAGLevel (A, AA, AAA), ComplianceTarget, ComplianceScope.
- Invariants: System MUST meet declared WCAGLevel (accessibility.inv.1).
- Triggers: compliance_violation, accessibility_regression.
- RULE: Declare WCAG compliance target (typically AA for most applications). Define ComplianceScope (full application, critical paths). Document exceptions with justification. Regular audits. New features must maintain compliance level.

## p2: Perceivable Content
```yaml
triggers: [missing_alt_text, decorative_not_marked]
requires_primitives: [Entity, Authority]
output_type: constraint
domain: a11y
category: other
```

- Primitives: AlternativeText (images, media), TextEquivalent, Transcript.
- Invariants: Non-text content MUST have text alternative (accessibility.inv.2).
- Triggers: missing_alt_text, decorative_not_marked.
- RULE: Images: meaningful alt text or empty alt for decorative. Audio: transcript. Video: captions and audio description. Complex images: long description. Charts: data table alternative. Test with screen readers.

## p3: Color and Contrast
```yaml
triggers: [contrast_failure, color_only_indication]
requires_primitives: [Entity, Authority]
output_type: constraint
domain: a11y
category: other
```

- Primitives: ContrastRatio (foreground, background), ColorIndependence.
- Invariants: Text contrast MUST meet WCAG ratio (4.5:1 normal, 3:1 large) (accessibility.inv.3).
- Triggers: contrast_failure, color_only_indication.
- RULE: Check contrast for all text. Don't rely on color alone for meaning (add icons, patterns, labels). Support high contrast mode. Test with color blindness simulators. Document color palette accessibility.

## p4: Keyboard Navigation
```yaml
triggers: [keyboard_trap, focus_lost, skip_missing]
requires_primitives: [Entity, Authority]
output_type: constraint
domain: a11y
category: other
```

- Primitives: FocusOrder, FocusIndicator, KeyboardTrap.
- Invariants: All functionality MUST be accessible via keyboard (accessibility.inv.4).
- Triggers: keyboard_trap, focus_lost, skip_missing.
- RULE: All interactive elements keyboard-accessible. Logical focus order (tab sequence). Visible focus indicator. No keyboard traps. Skip links for navigation. Test: Tab, Shift+Tab, Enter, Space, Escape, arrows.

## p5: ARIA Semantics
```yaml
triggers: [aria_misuse, missing_aria]
requires_primitives: [Entity, Authority]
output_type: constraint
domain: a11y
category: other
```

- Primitives: ARIARole, ARIAState, ARIAProperty, LiveRegion.
- Invariants: ARIA usage MUST not conflict with native semantics (accessibility.inv.5).
- Triggers: aria_misuse, missing_aria.
- RULE: Prefer native HTML semantics. Use ARIA for custom widgets. Roles: button, dialog, menu, etc. States: expanded, selected, checked. Properties: label, describedby. Live regions for dynamic content. Test with assistive technology.

## p6: Focus Management
```yaml
triggers: [focus_lost_on_action, modal_escape]
requires_primitives: [Entity, Authority]
output_type: constraint
domain: a11y
category: other
```

- Primitives: FocusContext, FocusTrap (modal), FocusRestore.
- Triggers: focus_lost_on_action, modal_escape.
- RULE: Manage focus on: page load, navigation, modal open/close, dynamic content. Trap focus in modals. Restore focus on modal close. Announce focus changes for screen readers. Avoid focus stealing.

## p7: Form Accessibility
```yaml
triggers: [unlabeled_field, error_not_announced]
requires_primitives: [Entity, Authority]
output_type: constraint
domain: a11y
category: other
```

- Primitives: FormLabel, FormError, FieldDescription, RequiredIndicator.
- Invariants: Form fields MUST have associated labels (accessibility.inv.6).
- Triggers: unlabeled_field, error_not_announced.
- RULE: Every input has visible, associated label. Required fields indicated (not just color). Error messages: associated with field, announced. Instructions before form. Group related fields with fieldset/legend. Accessible date pickers.

## p8: Screen Reader Support
```yaml
triggers: [content_skipped, wrong_announcement]
requires_primitives: [Entity, Authority]
output_type: constraint
domain: a11y
category: other
```

- Primitives: AnnouncementStrategy, ReadingOrder, HiddenContent.
- Triggers: content_skipped, wrong_announcement.
- RULE: Ensure logical reading order matches visual order. Hide decorative elements from screen readers (aria-hidden). Announce dynamic changes. Test with multiple screen readers (NVDA, JAWS, VoiceOver). Avoid "click here" links.

## p9: Motion and Animation
```yaml
triggers: [motion_sensitivity, flash_violation]
requires_primitives: [Entity, Authority]
output_type: constraint
domain: a11y
category: other
```

- Primitives: ReducedMotion, AnimationDuration, FlashThreshold.
- Invariants: Content MUST NOT flash more than 3 times per second (accessibility.inv.7).
- Triggers: motion_sensitivity, flash_violation.
- RULE: Respect prefers-reduced-motion media query. Provide pause/stop for auto-playing content. No flashing content (seizure risk). Animation duration reasonable. Essential animations only when reduced motion set.

## p10: Resize and Zoom
```yaml
triggers: [zoom_broken, text_cut_off]
requires_primitives: [Entity, Authority]
output_type: constraint
domain: a11y
category: other
```

- Primitives: TextResize (up to 200%), Reflow (320px width), ZoomSupport.
- Invariants: Content MUST be readable at 200% zoom without horizontal scroll (accessibility.inv.8).
- Triggers: zoom_broken, text_cut_off.
- RULE: Support text resize to 200% without loss of content. Reflow layout at narrow widths. Don't disable zoom on mobile. Use relative units (rem, em). Test at various zoom levels and viewport sizes.

## p11: Error Identification
```yaml
triggers: [error_not_perceivable]
requires_primitives: [Entity, Authority]
output_type: constraint
domain: a11y
category: other
```

- Primitives: ErrorAnnouncement, ErrorSummary, ErrorLink.
- Invariants: Errors MUST be announced and identifiable (accessibility.inv.9).
- Triggers: error_not_perceivable.
- RULE: On form error: announce error count, provide error summary, link to fields. Error messages adjacent to fields. Error state visually and programmatically indicated. Don't rely on color alone. Test error flows with screen readers.

## p12: Accessibility Testing
```yaml
triggers: [a11y_test_failed, regression_detected]
requires_primitives: [Entity, Authority]
output_type: constraint
domain: a11y
category: other
```

- Primitives: AutomatedTest (axe, WAVE), ManualTest, UserTest.
- Triggers: a11y_test_failed, regression_detected.
- RULE: Automated tests catch ~30% of issues. Manual testing: keyboard, screen reader, zoom. User testing with people with disabilities. Include accessibility in CI/CD. Regular audits (annual minimum). Document testing procedures.

## p13: Documentation and Training
```yaml
triggers: [statement_outdated]
requires_primitives: [Entity, Authority]
output_type: constraint
domain: a11y
category: other
```

- Primitives: AccessibilityStatement, VPATReport, TrainingProgram.
- Triggers: statement_outdated.
- RULE: Publish AccessibilityStatement with: compliance level, known issues, contact. Create VPAT for procurement (enterprise). Train developers on accessibility. Include accessibility in design reviews. Maintain accessibility backlog.
