# Frontend - Risk Assessment Dashboard

React application for managing companies and risk assessment requests.

## Development

### Setup
```bash
npm install
npm start
```

The application will be available at: http://localhost:3000

### Build for Production
```bash
npm run build
```

## Deployment

### Vercel (Recommended)
1. Connect your GitHub repository to Vercel
2. Set environment variables:
   - `NEXT_PUBLIC_API_URL`: Your backend API URL
   - `NEXT_PUBLIC_API_VERSION`: API version (v1)
3. Deploy automatically on git push

### Manual Deployment
```bash
npm run build
# Upload build/ directory to your hosting provider
```

## Environment Variables

Create `.env.local` file:
```bash
NEXT_PUBLIC_API_URL=http://localhost:8000
NEXT_PUBLIC_API_VERSION=v1
```

## Features

- [x] User authentication (login/register)
- [x] Companies management
- [x] Risk assessment requests
- [x] Responsive design
- [x] API integration

## Tech Stack

- React 18
- TypeScript (optional)
- Axios (HTTP client)
- Tailwind CSS (styling)
- React Router (navigation)

## Project Structure
```
src/
├── components/          # Reusable components
├── pages/               # Application pages
├── services/            # API integration
├── utils/               # Utility functions
└── styles/              # CSS styles
```
