# tsconfig.json

原始格式: JSON

```json
{
	"extends": "../tsconfig.json",
	"compilerOptions": {
		"types": ["@cloudflare/vitest-pool-workers"]
	},
	"include": ["./**/*.ts", "../worker-configuration.d.ts"],
	"exclude": []
}

```
