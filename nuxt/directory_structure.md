# Nuxt 3 Template Directory Structure

```
nuxt/
├── docker/
│   └── Dockerfile                      # Node.js 22 Alpine based Docker configuration
├── assets/
│   └── css/
│       └── main.css                    # Tailwind CSS global styles
├── components/
│   ├── Counter.vue                     # Counter component with Pinia
│   └── Counter.test.ts                 # Counter component tests
├── composables/
│   └── useUrqlClient.ts                # urql GraphQL client composable
├── layouts/
│   └── default.vue                     # Default layout with header and footer
├── pages/                              # File-based routing
│   ├── index.vue                       # Homepage (/)
│   ├── about.vue                       # About page (/about)
│   ├── graphql.vue                     # GraphQL CSR example (/graphql)
│   └── prisma.vue                      # Prisma SSR example (/prisma)
├── server/
│   └── api/
│       └── users.get.ts                # API route for fetching users (SSR)
├── stores/
│   ├── counter.ts                      # Pinia counter store
│   └── counter.test.ts                 # Counter store tests
├── lib/
│   └── prisma/
│       ├── client.ts                   # Prisma client singleton
│       └── schema.prisma               # Database schema (User, Post models)
├── test/                               # Test configuration
│   ├── setup.ts                        # Vitest global setup
│   └── example.test.ts                 # Sample tests
├── public/                             # Static files
│   └── favicon.svg                     # Site favicon
├── .env.example                        # Environment variables template
├── .gitignore                          # Git ignore rules
├── .node-version                       # Node.js version (22)
├── app.vue                             # Root app component
├── docker-compose.yml                  # Docker Compose setup (PostgreSQL + Nuxt)
├── nuxt.config.ts                      # Nuxt configuration
├── package.json                        # Dependencies and scripts
├── tailwind.config.js                  # Tailwind CSS configuration
├── tsconfig.json                       # TypeScript configuration
├── vitest.config.ts                    # Vitest testing configuration
└── README.md                           # Documentation
```

## Key Features

- **Full SSR Support**: Server-side rendering for SEO and performance
- **Auto Imports**: Components, composables, and utilities automatically imported
- **File-based Routing**: Pages automatically created from `pages/` directory
- **API Routes**: Server-side API endpoints in `server/api/`
- **Pinia Integration**: Official state management for Vue 3
- **urql GraphQL**: Client-side GraphQL data fetching
- **Prisma ORM**: Type-safe database access via API routes
- **Vitest Testing**: Fast unit and component testing
- **Docker Support**: Full containerization with PostgreSQL

## Rendering Modes

- **SSR (Default)**: Server-side rendering
- **SPA**: Single-page application mode
- **SSG**: Static site generation with `npm run generate`

## Test File Naming Convention

- Component tests: `ComponentName.test.ts`
- Store tests: `storeName.test.ts`
- Utility tests: `utilityName.test.ts`
- Example: `Counter.test.ts`, `counter.test.ts`, `example.test.ts`
