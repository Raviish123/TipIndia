import { createRootRouteWithContext, createRoute } from "@tanstack/react-router";
import { Home } from "./pages/Home";
import { Root } from "./components/Root";
import { Customer } from "./pages/Customer";
import { EmployeeRegister } from "./pages/EmployeeRegister";
import { CustomerPayment } from "./pages/CustomerPayment";
import { Manager } from "./pages/Manager";
import { getEmployee, getEmployees } from "./queries/queries";
import { QueryClient } from "@tanstack/react-query";
import { ErrorRoute } from "./components/ErrorRoute";


const rootRoute = createRootRouteWithContext<{queryClient: QueryClient}>() ({
    component: Root
});

const indexRoute = createRoute({
    getParentRoute: () => rootRoute,
    path: "/",
    component: Home,
})

// const loginRoute


// For customers to view employees to tip
const customerRoute = createRoute({
    getParentRoute: () => rootRoute,
    path: "/org/$org_id",
    errorComponent: ErrorRoute,
    component: Customer,
    loader: ({ context: { queryClient }, params }) => queryClient.ensureQueryData(getEmployees(params.org_id))
})


// For employees to register
const employeeRoute = createRoute({
    getParentRoute: () => rootRoute,
    path: "/employee/$org_id",
    errorComponent: ErrorRoute,
    component: EmployeeRegister,
    loader: ({ context: { queryClient }, params }) => queryClient.ensureQueryData(getEmployees(params.org_id))
})


// For customers to finalize their payment to the employees
const paymentRoute = createRoute({
    getParentRoute: () => rootRoute,
    path: "/tip/$employee_id",
    component: CustomerPayment,
    loader: ({ context: { queryClient }, params }) => queryClient.ensureQueryData(getEmployee(params.employee_id))
})


// For managers to delete employees and view stats, use token to get org
const adminRoute = createRoute({
    getParentRoute: () => rootRoute,
    path: "/admin",
    component: Manager
})



export const routeTree = rootRoute.addChildren([
    indexRoute,
    customerRoute,
    employeeRoute,
    paymentRoute,
    adminRoute
]);