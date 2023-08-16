import {getNumber} from './utils'

describe('getNumber', () => {
  it('parses a number', () => {
    expect(getNumber('1')).toBe(1)
    expect(getNumber('aa1')).toBe(1)
    expect(getNumber('1bb')).toBe(1)
    expect(getNumber('aa1bb')).toBe(1)
    expect(getNumber('aa123bb')).toBe(123)
  })
  it('throws an error if the text does not contain a number', () => {
    expect(() => getNumber('')).toThrowError(/Could not parse text/)
  })
})
