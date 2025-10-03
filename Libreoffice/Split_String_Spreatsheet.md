
### Formulas
Assuming your data is in column E (e.g., "6933 Kibæk" in E2), let’s use the following formulas, adjusted for clarity and to handle potential locale issues:

1. **Postnummer (postal code) in F2**:
   ```
   =LEFT(E2;FIND(" ";E2)-1)
   ```
   This extracts the text before the first space (e.g., "6933").

2. **By (city) in G2**:
   ```
   =RIGHT(E2;LEN(E2)-FIND(" ";E2))
   ```
   This extracts the text after the first space (e.g., "Kibæk").

**Note**: If your LibreOffice uses commas (`,`) instead of semicolons (`;`) as argument separators (common in some locales like US English), use these instead:
- For F2:
  ```
  =LEFT(E2,FIND(" ",E2)-1)
  ```
- For G2:
  ```
  =RIGHT(E2,LEN(E2)-FIND(" ",E2))
  ```

### Troubleshooting Steps
If you’re still getting Err:508, try these checks:

1. **Check for Spaces**:
   - Ensure the data in column E (e.g., E2) actually contains a space. For example, "6933 Kibæk" should have a single space between "6933" and "Kibæk".
   - If there’s no space or multiple spaces, the `FIND` function may fail. To handle this, use `TRIM` to clean up extra spaces:
     - For F2:
       ```
       =LEFT(TRIM(E2);FIND(" ";TRIM(E2))-1)
       ```
     - For G2:
       ```
       =RIGHT(TRIM(E2);LEN(TRIM(E2))-FIND(" ";TRIM(E2)))
       ```

2. **Verify Data**:
   - Click on a cell in column E (e.g., E2) and check if the text appears as expected (e.g., "6933 Kibæk").
   - If the data is imported or copied, there might be hidden characters (e.g., non-breaking spaces). To test, manually type "6933 Kibæk" in a cell and try the formula again.

3. **Locale Settings**:
   - In some locales, LibreOffice uses semicolons (`;`) instead of commas (`,`) to separate function arguments. If the above formulas with semicolons don’t work, try the comma versions (or vice versa).
   - To check your locale, go to **Tools > Options > LibreOffice Calc > Formula** and look at the "Separators" settings.

4. **Test the FIND Function Alone**:
   - In a blank cell, enter `=FIND(" ";E2)` (or with a comma: `=FIND(" ",E2)`) to see if it returns a number (the position of the space). If it returns an error, the space may not exist or may be a different character.

5. **Alternative: Text to Columns**:
   If formulas continue to fail, you can use LibreOffice’s **Text to Columns** feature to split the data without formulas:
   - Select column E.
   - Go to **Data > Text to Columns**.
   - Choose **Separated by**, select **Space**, and click **OK**.
   - This will split the data into columns F (Postnummer) and G (By) automatically.

### Example Output
For your data in column E:
| E             | F         | G           |
|---------------|-----------|-------------|
| Post/By       | Postnummer| By          |
| 6933 Kibæk    | 6933      | Kibæk       |
| 6818 Årre     | 6818      | Årre        |
| 8381 Mundelstrup | 8381   | Mundelstrup |
| 8000 Århus C  | 8000      | Århus C     |

### Next Steps
- Try the formulas with the correct separator (`,` or `;`) for your locale.
- If you still get Err:508, please:
  1. Share the exact formula you’re using.
  2. Confirm the exact text in one of the cells (e.g., E2).
  3. Let me know your LibreOffice locale or separator settings.
- If you prefer the Text to Columns method or need help with a macro for automation, let me know!
