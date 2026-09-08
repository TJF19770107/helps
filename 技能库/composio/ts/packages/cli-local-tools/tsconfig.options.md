# tsconfig.options.json

原始格式: JSON

```json
{
  "$schema": "https://json.schemastore.org/tsconfig",
  "extends": "../../../tsconfig.base.json",
  "compilerOptions": {
    "declaration": true,
    "outDir": "./dist",
    "rootDir": ".",
    "strict": true,
    "esModuleInterop": true,
    "moduleResolution": "bundler",
    "skipLibCheck": true,
    "resolveJsonModule": true,
    "verbatimModuleSyntax": true,
    "pretty": true,
    "noImplicitReturns": true,
    "noFallthroughCasesInSwitch": true,
    "noUnusedLocals": false,
    "noUnusedParameters": false,
    "types": ["node"]
  },
  "include": ["src"],
  "exclude": ["**/dist", "test/__fixtures__/**"]
}

```
