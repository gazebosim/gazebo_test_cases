import type Step from './Step'

type Check = {
  name: string
  description?: string
  try?: Step[]
  expect?: Step[]
}

export default Check
