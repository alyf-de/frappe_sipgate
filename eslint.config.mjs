import { createRequire } from "node:module";

const require = createRequire(import.meta.url);
// Use CJS resolver so pre-commit NODE_PATH is honored.
const globals = require("globals");
const js = require("@eslint/js");

export default [
	js.configs.recommended,
	{
		languageOptions: {
			ecmaVersion: 2022,
			sourceType: "module",
			globals: {
				...globals.browser,
				frappe: "readonly",
				__: "readonly",
			},
		},
	},
];
