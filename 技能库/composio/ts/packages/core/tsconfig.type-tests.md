# tsconfig.type-tests.json

原始格式: JSON

```json
{
  "extends": "./tsconfig.json",
  "compilerOptions": {
    "noEmit": true,
    "rootDir": "."
  },
  "include": ["src/**/*.ts", "type-tests/**/*.ts", "type-tests/**/*.d.ts", "package.json"]
}

```
