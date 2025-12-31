# Astro Template Directory Structure

```
astro/
├── docker/
│   └── Dockerfile                      # Node.js 22 Alpine based Docker configuration
├── public/                             # Static assets served as-is
│   └── favicon.svg                     # Site favicon
├── src/
│   ├── components/                     # Reusable components
│   │   ├── Counter.tsx                 # React interactive counter example
│   │   └── Counter.test.tsx            # Counter component tests
│   ├── layouts/
│   │   └── Layout.astro                # Base HTML layout
│   ├── pages/                          # File-based routing
│   │   ├── index.astro                 # Homepage (/)
│   │   ├── about.astro                 # About page (/about)
│   │   └── blog/
│   │       └── index.astro             # Blog listing page (/blog)
│   ├── lib/
│   │   └── prisma/                     # Database ORM
│   │       ├── client.ts               # Prisma client singleton
│   │       └── schema.prisma           # Database schema (User, Post models)
│   ├── styles/
│   │   └── global.css                  # Global styles with Tailwind directives
│   ├── test/                           # Test configuration
│   │   ├── setup.ts                    # Vitest global setup
│   │   └── example.test.ts             # Sample tests
│   └── env.d.ts                        # TypeScript environment definitions
├── .env.example                        # Environment variables template
├── .gitignore                          # Git ignore rules
├── .node-version                       # Node.js version (22)
├── astro.config.mjs                    # Astro configuration
├── docker-compose.yml                  # Docker Compose setup (PostgreSQL + Astro)
├── package.json                        # Dependencies and scripts
├── tailwind.config.mjs                 # Tailwind CSS configuration
├── tsconfig.json                       # TypeScript configuration
├── vitest.config.ts                    # Vitest testing configuration
└── README.md                           # Documentation
```

## Key Features

- **Static Site Generation (SSG)**: Default output mode for maximum performance
- **Islands Architecture**: Only necessary JavaScript is shipped to the client
- **File-based Routing**: Pages automatically created from `src/pages/` structure
- **React Integration**: Interactive components with `client:*` directives
- **MDX Support**: Markdown with embedded components
- **Prisma ORM**: Type-safe database access
- **Vitest Testing**: Fast unit and component testing
- **Docker Support**: Full containerization with PostgreSQL

## Test File Naming Convention

- Component tests: `ComponentName.test.tsx`
- Utility tests: `utilityName.test.ts`
- Example: `Counter.test.tsx`, `example.test.ts`
