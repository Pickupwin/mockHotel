// frontend/hotel-booking/src/api/ftInvoke.ts
import axios from 'axios'

export function ftInvoke(body: {
  app_id: number,
  path: string,
  name: string,
  mode?: string,
  provider?: string,
}) {
  return axios({
    url: '/ft/invoke',
    method: 'post',
    data: body
  })
}