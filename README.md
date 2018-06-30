# Currency converter

Currency converter using forex(https://github.com/MicroPyramid/forex-python)

Input parameters:
  --amount - amount which we want to convert - float
  --input_currency - input currency - 3 letters name or currency symbol
  --output_currency - requested/output currency - 3 letters name or currency symbol
  
If output currency is missing, convert to all know currencies. 
If input/output currency is symbol, which is valid for more currency codes, convert from/to all valid currencies. 
Support for 34 currency codes and 24 currency symbols.
