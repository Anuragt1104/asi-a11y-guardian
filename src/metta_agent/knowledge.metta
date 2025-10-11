(Issue missing_lang)
(SC missing_lang "3.1.1" "Language of Page")
(Fix missing_lang "Add a valid lang attribute to the <html> tag, e.g., <html lang=\"en\">.")
(Refs missing_lang ("https://www.w3.org/WAI/WCAG21/Understanding/language-of-page/" "https://developer.mozilla.org/en-US/docs/Web/HTML/Global_attributes/lang"))
(Severity missing_lang high)

(Issue missing_title)
(SC missing_title "2.4.2" "Page Titled")
(Fix missing_title "Add a <title> element that concisely describes the page purpose.")
(Refs missing_title ("https://www.w3.org/WAI/WCAG21/Understanding/page-titled/" "https://developer.mozilla.org/en-US/docs/Web/HTML/Element/title"))
(Severity missing_title medium)

(Issue missing_alt)
(SC missing_alt "1.1.1" "Non-text Content")
(Fix missing_alt "Provide meaningful alt text describing the image purpose.")
(Refs missing_alt ("https://www.w3.org/WAI/WCAG21/Understanding/non-text-content/" "https://webaim.org/techniques/alttext/"))
(Severity missing_alt high)

(Issue headings_order)
(SC headings_order "2.4.6" "Headings and Labels")
(Fix headings_order "Ensure headings follow a logical outline (no jumps, start at <h1>).")
(Refs headings_order ("https://www.w3.org/WAI/WCAG21/Understanding/headings-and-labels/" "https://developer.mozilla.org/en-US/docs/Web/HTML/Element/Heading_Elements"))
(Severity headings_order medium)

(Issue missing_label)
(SC missing_label "3.3.2" "Labels or Instructions")
(Fix missing_label "Associate inputs with visible labels or aria-label/aria-labelledby.")
(Refs missing_label ("https://www.w3.org/WAI/WCAG21/Understanding/labels-or-instructions/" "https://developer.mozilla.org/en-US/docs/Web/Accessibility/ARIA/Attributes/aria-label"))
(Severity missing_label high)

(Issue bad_link_text)
(SC bad_link_text "2.4.4" "Link Purpose (In Context)")
(Fix bad_link_text "Use descriptive link text that indicates the link destination or purpose.")
(Refs bad_link_text ("https://www.w3.org/WAI/WCAG21/Understanding/link-purpose-in-context/" "https://www.w3.org/WAI/tutorials/page-structure/links/"))
(Severity bad_link_text low)

; Query: map issue code -> SC, Title, Severity, Fix, Refs
(= (map-issue $code $sc $title $severity $fix $refs)
   (match &self
     (,
       (Issue $code)
       (SC $code $sc $title)
       (Severity $code $severity)
       (Fix $code $fix)
       (Refs $code $refs)
     )
     (Result $sc $title $severity $fix $refs)
   )
)
