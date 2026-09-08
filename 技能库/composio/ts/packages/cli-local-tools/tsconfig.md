# tsconfig.json

原始格式: JSON

```json
{
  "extends": "./tsconfig.src.json",
  "compilerOptions": {
    "composite": true,
    "rootDir": "./src"
  },
  "include": ["src/**/*.ts"],
  "exclude": ["src/**/*.test.ts", "dist"]
}

```
