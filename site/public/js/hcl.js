// HCL of Terraform and OpenTofu, which highlight.js and its languages do not
// have, for the files .tf of the examples
window.hljs?.registerLanguage("hcl", (hljs) => ({
  name: "HCL",
  aliases: ["terraform", "tf"],
  keywords: {
    keyword:
      "resource data variable output locals module provider terraform moved import removed check for in if",
    literal: "true false null",
  },
  contains: [
    hljs.HASH_COMMENT_MODE,
    hljs.C_LINE_COMMENT_MODE,
    hljs.C_BLOCK_COMMENT_MODE,
    {
      className: "string",
      begin: /<<-?EO[FT]$/,
      end: /^\s*EO[FT]$/,
    },
    {
      className: "string",
      begin: /"/,
      end: /"/,
      contains: [
        hljs.BACKSLASH_ESCAPE,
        { className: "subst", begin: /\$\{/, end: /\}/ },
      ],
    },
    // The name of an attribute, before its =
    { className: "attr", begin: /\b[A-Za-z_][\w-]*(?=\s*=(?!=))/ },
    hljs.NUMBER_MODE,
  ],
}));
