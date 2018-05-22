from fri3d import badge
import utime

# -- set the row counter
r = 0

# -- we will run through each row of the matrices
while True:
    # -- make sure we are not going out of our row range by taking the rest of r / 5, which is always between -1 < x < 5
    r %= 5

    # -- clear both matrices
    badge.matrix().clear(0)
    badge.matrix().clear(1)

    # -- run through all the columns in the matrix to set their pixels
    for c in range(0, 7):
        for m in range(0, 7):
            badge.matrix().set(m, c, r)

    # -- go to the next row
    r += 1

    # -- sleep for 1 second
    utime.sleep(1)
