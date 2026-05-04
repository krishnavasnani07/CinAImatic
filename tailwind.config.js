/** @type {import('tailwindcss').Config} */
export default {
  darkMode: "class",
  content: [
    "./index.html",
    "./screens/**/*.html"
  ],
  theme: {
    extend: {
      "colors": {
        "error": "#ffb4ab",
        "primary": "#c8c6c5",
        "tertiary": "#ffb4aa",
        "primary-container": "#121212",
        "on-error-container": "#ffdad6",
        "on-primary-fixed-variant": "#474646",
        "error-container": "#93000a",
        "inverse-primary": "#5f5e5e",
        "secondary-container": "#fabd00",
        "surface-dim": "#131313",
        "surface-container-low": "#1b1c1c",
        "on-primary-fixed": "#1c1b1b",
        "primary-fixed-dim": "#c8c6c5",
        "secondary-fixed": "#ffdf9e",
        "on-error": "#690005",
        "on-tertiary-fixed-variant": "#930007",
        "on-tertiary-fixed": "#410001",
        "outline": "#8e9192",
        "outline-variant": "#444748",
        "on-surface": "#e4e2e1",
        "surface-tint": "#c8c6c5",
        "on-secondary": "#3f2e00",
        "on-surface-variant": "#c4c7c7",
        "on-tertiary": "#690003",
        "surface": "#131313",
        "on-secondary-container": "#6a4e00",
        "surface-container-high": "#2a2a2a",
        "inverse-surface": "#e4e2e1",
        "surface-bright": "#393939",
        "tertiary-fixed-dim": "#ffb4aa",
        "tertiary-container": "#2f0001",
        "on-secondary-fixed-variant": "#5b4300",
        "secondary": "#ffdf9e",
        "surface-container": "#1f2020",
        "tertiary-fixed": "#ffdad5",
        "on-background": "#e4e2e1",
        "on-tertiary-container": "#f61f1f",
        "on-secondary-fixed": "#261a00",
        "primary-fixed": "#e5e2e1",
        "on-primary": "#313030",
        "background": "#131313",
        "on-primary-container": "#7e7d7d",
        "surface-container-highest": "#353535",
        "secondary-fixed-dim": "#fabd00",
        "surface-variant": "#353535",
        "surface-container-lowest": "#0e0e0e",
        "inverse-on-surface": "#303030"
      },
      "borderRadius": {
        "DEFAULT": "0.25rem",
        "lg": "0.5rem",
        "xl": "0.75rem",
        "full": "9999px"
      },
      "spacing": {
        "stack-sm": "8px",
        "gutter-card": "16px",
        "margin-page": "24px",
        "stack-md": "16px",
        "stack-lg": "32px",
        "unit": "4px"
      },
      "fontFamily": {
        "headline-md": ["Be Vietnam Pro"],
        "title-sm": ["Inter"],
        "label-caps": ["Inter"],
        "body-md": ["Inter"],
        "display-lg": ["Be Vietnam Pro"]
      },
      "fontSize": {
        "headline-md": ["24px", {"lineHeight": "32px", "fontWeight": "700"}],
        "title-sm": ["18px", {"lineHeight": "24px", "fontWeight": "600"}],
        "label-caps": ["12px", {"lineHeight": "16px", "letterSpacing": "0.1em", "fontWeight": "700"}],
        "body-md": ["16px", {"lineHeight": "24px", "fontWeight": "400"}],
        "display-lg": ["40px", {"lineHeight": "48px", "letterSpacing": "-0.02em", "fontWeight": "800"}]
      }
    },
  },
  plugins: [],
}

