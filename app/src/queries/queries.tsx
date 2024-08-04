import { queryOptions } from "@tanstack/react-query";
import { getEmployeeApiEmployeeEmployeeIdGet, getEmployeesByOrganizationApiEmployeeOrganizationOrganizationIdGet } from "../client";

export function getEmployees(org_id: string) {
    return queryOptions({
        queryKey: ["get_employees"],
        queryFn: () => getEmployeesByOrganizationApiEmployeeOrganizationOrganizationIdGet({path: { organization_id: org_id}})
    })
}


export function getEmployee(employee_id: string) {
    return queryOptions({
        queryKey: ["get_employee"],
        queryFn: () => getEmployeeApiEmployeeEmployeeIdGet({path: { employee_id: employee_id}})
    })
}