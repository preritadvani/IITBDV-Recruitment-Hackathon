<h1>Data Assosciation</h1>:<br>
The problem with Greedy Algorithm:<br>
We need to assign exactly one Blue cone to a Yellow cone and vise versa. If we just try to assign the closest yellow cone to each blue cone we may end up assigning a cone twice.<br>
How is the used algorithm better?<br>
It solves the given problem: Given a cost matrix, find the one-to-one assignment of rows to columns that minimises total cost. No two rows can share a column.<br>
How it works?<br>
Step 1 — Row Reduction<br>
Subtract the minimum of each row from that row.<br>
Step 2 — Column Reduction<br>
Subtract the minimum of each column from that column<br>
Step 3 — Cover all zeros with minimum lines<br>
Find the minimum number of lines (rows + columns) that cover all zeros:<br>
Step 4 — Create new zeros
<br>
i. Find the smallest uncovered value (not under any line).<br>
ii. Subtract it from all uncovered values<br>
iii. Add it to values covered by two lines<br>
Step 5 — Repeat Step 3<br>
Cover all zeros again:<br>
Step 6 — Read the assignment<br>
Find an assignment using only zeros (one per row, one per column)<br>
