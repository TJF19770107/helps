# tsconfig.test.json

原始格式: JSON

```json
{
  "$schema": "https://json.schemastore.org/tsconfig",
  "extends": "./tsconfig.options.json",
  "compilerOptions": {
    "rootDir": ".",
    "paths": {
      "src/*": ["./src/*"],
      "test/*": ["./test/*"]
    }
  },
  "include": ["test"]
}

```
