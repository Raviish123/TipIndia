import { useMutation, useQueryClient, useSuspenseQuery } from "@tanstack/react-query"
import { useForm, SubmitHandler } from "react-hook-form"
import { getEmployees } from "../queries/queries"
import { useNavigate, useParams } from "@tanstack/react-router"
import { createEmployeeApiEmployeePost, CreateEmployeeApiEmployeePostError, EmployeeCreate } from "../client"


export function EmployeeRegister() {

    const queryClient = useQueryClient()

    const navigate = useNavigate()
    

    const {
        register,
        handleSubmit,
        reset,
        formState: { errors, isSubmitting },
      } = useForm<EmployeeCreate>({
        mode: "onBlur",
        defaultValues: {
            name: "",
            upi_id: "",
            organization_id: useParams({ strict: false}).org_id!
        }
    })

    const createMutation = useMutation({
        mutationFn: (data: EmployeeCreate) => createEmployeeApiEmployeePost({ body: data }),
        onSuccess: () => {
            alert("Employee Created Successfully!")
            reset()
            navigate({to: "/"})
        },
        onError: (err: CreateEmployeeApiEmployeePostError) => {
            const errDetail = err.detail
            alert("Something went wrong. " + `${errDetail}`)
        },
        onSettled: () => {
            queryClient.invalidateQueries({ queryKey: ["get_employees"] })
        },
    })

    const onSubmit: SubmitHandler<EmployeeCreate> = (data) => createMutation.mutate(data)
    
    const { data, error, isFetching } = useSuspenseQuery(getEmployees(useParams({ strict: false}).org_id!))

    if (error && !isFetching) return <>Error {error.message}</>
    if (data.error) return <>Error {data.error.detail}</>



    return (
    <>
        <h1>Register with your UPI ID, Name and Photo</h1>
        <h2>{data.data.organization_name}</h2>
        <h3>{data.data.organization_description}</h3>

        <form onSubmit={handleSubmit(onSubmit)}>
            <label htmlFor="name"></label>
            <input id="name" {...register("name", { required: "Full Name is required."})} placeholder="Enter Full Name" type="text" />
            {errors.name && <p>{errors.name.message}</p>}

            <label htmlFor="upi_id"></label>
            <input id="upi_id" {...register("upi_id", { required: "UPI ID is required."})} placeholder="Enter UPI ID (e.g. 1234567890@paytm)" type="text" />
            {errors.upi_id && <p>{errors.upi_id.message}</p>}

            <button type="submit" disabled={isSubmitting}>Submit</button>
        </form>
    
    </>
    
    // TODO: Show all employees at the restaurant maybe.
    )
}