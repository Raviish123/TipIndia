import { useSuspenseQuery } from "@tanstack/react-query"
import { Link, useParams } from "@tanstack/react-router"
import { getEmployees } from "../queries/queries"


export function Customer() {

    // const organization_employees = routeApi.useLoaderData()
    // TODO: Fix errors, or create a proper error component
    const { data, error, isFetching } = useSuspenseQuery(getEmployees(useParams({ strict: false}).org_id!))


    if (error && !isFetching) return <>Error {error.message}</>
    if (data.error) return <>Error {data.error.detail}</>

    const employees = data.data

    // employees.organization_name
    // employees.organization_description


    return (
    <>

    Choose an employee

    {employees.data?.map( employee => (
        <>
            <br />
            <li key={employee.employee_id}>
                <Link
                    to="/tip/$employee_id"
                    params= {{
                        employee_id: employee.employee_id!
                    }}>
                    {employee.name}
                </Link>     
            </li>

        </>
    ))}


    </>
    )
}