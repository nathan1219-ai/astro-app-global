import http from './http'

export async function calcFate(name: string, birthday: string) {
  const r = await http.post('/calc', { name, birthday, calendar: 'gregorian' })
  return r.data
}

export async function cardElements(sign: string, zodiac: string, element: string) {
  const r = await http.get('/card-elements', { params: { sign, zodiac, element } })
  return r.data
}
