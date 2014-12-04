import os, time

f = open("results.csv", "w+")
for s in range(1, 6):
  count = 10
  result = 0
  seconds = 0
  for _ in range(0, count):
    start = time.time()
    run_string = "python tsp.py -i example-input-1.txt -s " + str(s)
    result += int(os.popen(run_string).read())
    end = time.time()
    seconds += (end - start)
  avg_result = result / count
  avg_seconds = seconds / count
  f.write(str(s) + "," + str(avg_result) + "," + str(avg_seconds) + "\n")
f.close()
