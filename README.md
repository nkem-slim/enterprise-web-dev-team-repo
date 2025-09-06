# Team Name: Adventure

## Project Description

This project is an enterprise-level fullstack application designed to process MoMo SMS data in XML format. The system will clean and categorize the data, store it in a relational database, and provide a comprehensive frontend interface for data analysis and visualization.

## Team Members

- Nkem Vincent Nweke
- Yusuf Nabide
- Ibrahim Maazou Djahadi

## Project Structure (Mono-repo)

```
├── README.md                         # Project overview and setup
├── package.json                      # Root package.json for workspace management
├── .gitignore                        # Root gitignore
├── backend/                          # Backend API and data processing (TypeScript)
│   ├── package.json                  # Backend dependencies
│   ├── tsconfig.json                 # TypeScript configuration
│   ├── env.example                   # Environment variables template
│   ├── .gitignore                    # Backend gitignore
│   ├── README.md                     # Backend documentation
│   ├── src/                          # Backend source code
│   │   ├── index.ts                  # Main entry point
│   │   ├── app.ts                    # Express app configuration
│   │   ├── server.ts                 # Server startup logic
│   │   ├── api/                      # API routes and controllers
│   │   │   ├── routes.ts
│   │   │   └── controllers.ts
│   │   ├── services/                 # Business logic services
│   │   │   ├── database.ts
│   │   │   └── etl.ts
│   │   ├── models/                   # Database models and schemas
│   │   │   ├── sms.ts
│   │   │   └── transaction.ts
│   │   ├── etl/                      # ETL pipeline modules
│   │   │   ├── parser.ts
│   │   │   ├── cleaner.ts
│   │   │   └── categorizer.ts
│   │   ├── middleware/               # Express middleware
│   │   │   ├── cors.ts
│   │   │   └── logger.ts
│   │   ├── config/                   # Configuration files
│   │   │   ├── database.ts
│   │   │   └── app.ts
│   │   └── utils/                    # Utility functions
│   │       ├── validation.ts
│   │       └── helpers.ts
│   ├── data/                         # Data storage
│   │   ├── raw/                      # Raw XML input files
│   │   ├── processed/                # Processed data outputs
│   │   └── logs/                     # ETL logs and dead letter queue
│   ├── tests/                        # Backend tests
│   └── docs/                         # Backend documentation
├── frontend/                         # React frontend application (JavaScript)
│   ├── package.json                  # Frontend dependencies
│   ├── vite.config.js                # Vite configuration
│   ├── eslint.config.js              # ESLint configuration
│   ├── index.html                    # HTML entry point
│   ├── public/                       # Static assets
│   │   └── vite.svg
│   ├── src/                          # Frontend source code
│   │   ├── main.jsx                  # React entry point
│   │   ├── App.jsx                   # Main App component
│   │   ├── App.css                   # App styles
│   │   ├── index.css                 # Global styles
│   │   ├── components/               # React components
│   │   │   ├── Dashboard.jsx
│   │   │   ├── Charts.jsx
│   │   │   └── DataTable.jsx
│   │   ├── pages/                    # Page components
│   │   │   ├── Home.jsx
│   │   │   └── Analytics.jsx
│   │   ├── hooks/                    # Custom React hooks
│   │   │   └── useData.js
│   │   ├── services/                 # API services
│   │   │   └── api.js
│   │   ├── utils/                    # Utility functions
│   │   │   └── helpers.js
│   │   ├── contexts/                 # React contexts
│   │   └── assets/                   # Static assets
│   │       ├── images/
│   │       └── icons/
│   └── dist/                         # Built frontend files
├── shared/                           # Shared utilities and types
│   ├── package.json                  # Shared package configuration
│   ├── types/                        # TypeScript type definitions
│   │   ├── index.ts
│   │   ├── sms.ts
│   │   └── api.ts
│   ├── utils/                        # Shared utility functions
│   │   └── index.ts
│   └── constants/                    # Shared constants
│       └── index.ts
├── docs/                             # Project documentation
│   ├── ARCHITECTURE.md
│   ├── API.md
│   └── DEPLOYMENT.md
└── scripts/                          # Build and deployment scripts
    ├── build.sh
    ├── dev.sh
    └── deploy.sh
```

## Technology Stack

- **Frontend**: React + Vite + TypeScript
- **Backend**: Node.js + Express + TypeScript
- **Database**: SQLite
- **Data Processing**: XML parsing, data cleaning, categorization
- **Visualization**: Chart.js / Recharts

## Getting Started

### Prerequisites

- Node.js 18+
- npm or yarn
- Git

### Development Setup

1. **Install dependencies:**

   ```bash
   npm install
   ```

2. **Start development servers:**

   ```bash
   # Start both frontend and backend
   npm run dev

   # Or start individually
   npm run dev:frontend
   npm run dev:backend
   ```

3. **Build for production:**
   ```bash
   npm run build
   ```

## Trello Link
[Click me](https://trello.com/invite/b/68bc46e9caee3d10c730abdc/ATTI6e30dc2aa5e0630fccc415b09ece3feaEF219F6D/adventure)

## Architecture Diagram Link
[Click me](https://www.mermaidchart.com/app/projects/b70ecf6c-d680-473d-82bd-c2d9c298423f/diagrams/d257d5be-241f-454c-9552-1b62c08fcebc/version/v0.1/edit)

## Thank you
