// import { getRouteApi } from "@tanstack/react-router"

import { useMutation, useQueryClient, useSuspenseQuery } from "@tanstack/react-query"
import { getEmployee } from "../queries/queries"
import { useParams } from "@tanstack/react-router"
import { addTipApiTipsAddTipPost, AddTipApiTipsAddTipPostError, TipCreate } from "../client"
import { SubmitHandler, useForm } from "react-hook-form"



export function CustomerPayment() {

    const queryClient = useQueryClient()


    const {
        register,
        handleSubmit,
        reset,
        formState: { errors, isSubmitting },
      } = useForm<TipCreate>({
        mode: "onBlur",
        defaultValues: {
            amount: 0,
            employee_id: useParams({ strict: false}).employee_id!
        }
    })


    
    const { data, error, isFetching } = useSuspenseQuery(getEmployee(useParams({ strict: false}).employee_id!))
    const employee = data.data

    if (error && !isFetching) return <>Error {error.message}</>
    if (data.error) return <>Error {data.error.detail}</>

    const tipMutation = useMutation({
        mutationFn: (data: TipCreate) => addTipApiTipsAddTipPost({ body: data }),
        onSuccess: () => {
            alert("Tip Made Successfully!")
            reset()
            window.location.href = "upi://pay?pa=" + employee.upi_id + "&pn=" + employee.name + "&cu=INR"
        },
        onError: (err: AddTipApiTipsAddTipPostError) => {
            const errDetail = err.detail
            alert("Something went wrong. " + `${errDetail}`)
        },
        onSettled: () => {
            queryClient.invalidateQueries({ queryKey: ["get_employees"] })
        },
    })

    const onSubmit: SubmitHandler<TipCreate> = (data) => tipMutation.mutate(data)

    return (
    <>
        <h1>Tip {employee.name}!</h1>

        <form onSubmit={handleSubmit(onSubmit)}>
            <label htmlFor="amount"></label>
            <input id="amount" {...register("amount", { required: "Amount is required."})} placeholder="Enter amount to tip (Rs.)" min="0" type="number" />
            {errors.amount && <p>{errors.amount.message}</p>}

            <button type="submit" disabled={isSubmitting}>Submit</button>
        </form>
    </>
)
}