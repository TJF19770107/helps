# tsconfig.src.json

原始格式: JSON

```json
{
  "$schema": "https://json.schemastore.org/tsconfig",
  "extends": "./tsconfig.options.json",
  "compilerOptions": {
    "outDir": "./dist",
    "rootDir": "."
  },
  "include": ["src/**/*", "package.json"],
  "exclude": ["node_modules", "../../../node_modules", "**/dist"]
}

```
