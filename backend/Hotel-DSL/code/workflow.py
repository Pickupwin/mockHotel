from faasit_runtime import workflow, Workflow


@workflow
def hotelworkflow(wf: Workflow):
    s0 = wf.call('stage0-0', {
    })
    return s0

hotelworkflow = hotelworkflow.export()

