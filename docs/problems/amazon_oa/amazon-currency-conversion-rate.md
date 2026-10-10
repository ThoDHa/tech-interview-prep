# [Currency Conversion Rate](https://www.fastprep.io/problems/amazon-currency-conversion-rate)

**Medium** | **NN minutes** | **Graph, Breadth First Search, Hash Table**

You are given currency conversion rates. Each row contains a source currency, a target currency, and the value of one unit of the source currency in the target currency.

A conversion may use multiple rates. A listed rate may also be used in reverse by taking its reciprocal.

Given a query [from, to], return the conversion rate from from to to, rounded and formatted with exactly two digits after the decimal point. Every judged query is connected by the supplied rates.

## Examples

### Example 1

**Input:** `rates = [["USD","JPY","110"],["USD","AUD","1.45"],["JPY","GBP","0.0070"]]`, `query = ["GBP","AUD"]`

**Output:** `"1.88"`

**Explanation:** Use the reverse of JPY -> GBP, then the reverse of USD -> JPY, then USD -> AUD: (1 / 0.0070) * (1 / 110) * 1.45 = 1.883116.... Rounded to two decimal places, the result is 1.88.

### Example 2

**Input:** `rates = [["USD","CAD","1.30"],["CAD","EUR","0.70"]]`, `query = ["USD","EUR"]`

**Output:** `"0.91"`

**Explanation:** One USD is 1.30 CAD, and one CAD is 0.70 EUR, so the rate is 1.30 * 0.70 = 0.91.

## Constraints

<!-- Constraints not parseable from FastPrep for amazon-currency-conversion-rate; fill them in. -->

## Solutions

<!-- Scaffold placeholder: the worked derivation and solutions land
     on the solutions branch later. See ../_TEMPLATE.md for the
     expected layout, naming, and ordering conventions. -->
