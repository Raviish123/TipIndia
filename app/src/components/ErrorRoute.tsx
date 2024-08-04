import { ErrorComponentProps } from "@tanstack/react-router";

export function ErrorRoute({ error }: ErrorComponentProps) {
    return <div>{error.message}</div>
} 