import type Step from './Step'
import type Link from './Link'

type Requirement = {
  name: string
  description?: string
  labels?: string[]
  links?: Link[]
  steps: Step[]
}

export default Requirement
