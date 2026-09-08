# tsconfig.src.json

原始格式: JSON

```json
{
  "$schema": "https://json.schemastore.org/tsconfig",
  "extends": "./tsconfig.options.json",
  "compilerOptions": {
    "outDir": "./dist",
    "rootDir": ".",
    "paths": {
      "src/*": ["./src/*"]
    }
  },
  "include": ["src"],
  "exclude": ["src/**/*.test.ts"]
}

```
