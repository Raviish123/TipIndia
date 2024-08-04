import React from 'react'
import ReactDOM from 'react-dom/client'
import { QueryClient, QueryClientProvider } from '@tanstack/react-query'
import { createClient } from '@hey-api/client-axios';
import { createRouter, RouterProvider } from '@tanstack/react-router';
import { routeTree } from './routes';
import { Loader } from './components/Loader';


const queryClient = new QueryClient()

const router = createRouter({ 
  routeTree,
  defaultPendingMs: 200,
  defaultPendingMinMs: 1000,
  defaultPendingComponent: Loader,
  context: { queryClient }
})


declare module "@tanstack/react-router" {
  interface Register {
    router: typeof router
  }
}



// client for making requests with open api client
createClient({
  baseURL: "http://localhost:8000",  
})

ReactDOM.createRoot(document.getElementById('root')!).render(
  <React.StrictMode>
    <QueryClientProvider client={queryClient}>
      <RouterProvider router={router} />
    </QueryClientProvider>
  </React.StrictMode>,
)
