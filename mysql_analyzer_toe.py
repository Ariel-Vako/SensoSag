#!/usr/bin/python

import math
import MySQLdb
import struct
import matplotlib.pyplot as plt
import matplotlib.dates as mdates
import numpy as np
from scipy import signal, fftpack, optimize
from dateutil import parser

startDate = "2018-08-01 00:00"
endDate = "2018-08-30 00:00"

##CONFIG###################

toe_window_min = 90
toe_window_max = 180

packet_len = 520
# For dates

# Get the filter coefficients so we can check its frequency response.
b, a = signal.butter(3, 0.048)
# create timeframe for all samples
t = np.linspace(0, (packet_len - 1) * 0.02, packet_len)
# create auxiliary objects
clipped_data = np.zeros(packet_len)
virtual_impacts = np.zeros(packet_len)
impacts_mask = np.zeros(packet_len)

# impact threshold
threshold = 1

# functions
# fitfunc = lambda p, x: p[0]*np.cos(2*np.pi*p[1]*x+p[2]) + p[3]
fitfunc = lambda p, x: np.cos(2 * np.pi * p[1] * x + p[2]) + p[3]
errfunc = lambda p, x, y: fitfunc(p, x) - y
anglefunc = lambda p, x: ((2 * np.pi * p[1] * x + p[2]))  ## Radians
degfunc = lambda p, x: map(math.degrees, np.mod(((2 * np.pi * p[1] * x + p[2])), 2 * np.pi))  ## degrees


def process(results):
    # print(results)
    samples = []
    dates = []
    speeds = []
    hist2d = []
    impacts = []
    toe = []
    toe_std = []

    for row in results:
        #	print row
        sample = []
        for x in range(packet_len):
            sample.append(float((ord(row[0][x * 2]) << 8) + ord(row[0][x * 2 + 1]) - 2 ** 15) / 2 ** 8)
        # date = row[1]
        dates.append(row[1])

        ######################################################################

        for i in range(len(sample) - 1):
            if i == 0:
                virtual_impacts[i] = np.abs(sample[i])
            else:
                virtual_impacts[i] = np.abs(sample[i - 1] - sample[i])

        ##binarize sample to isolate impactless interval
        impacts_mask = np.where(virtual_impacts > threshold, 0, 1)

        # clip data between 1 [G] and -2 [G] range
        for i in range(len(sample) - 1):
            if sample[i] > 1:
                clipped_data[i] = 0
            elif sample[i] < -2:
                clipped_data[i] = -2
            else:
                clipped_data[i] = sample[i]

        ## Filter data with butterworth low-pass
        filtered_data = signal.filtfilt(b, a, clipped_data, method="pad", padtype="even")

        p0 = [1, 0.14, 0, -0.5]  # starting guess

        # fit filtered
        p1, success = optimize.leastsq(errfunc, p0[:], args=(t, filtered_data))

        if p1[1] < 0.1:
            filtered_data = np.flip(filtered_data, 0)  # what a fucking genius
            p1, success = optimize.leastsq(errfunc, p0[:], args=(t, filtered_data))
        # not needed, just to see the graph
        # sample = np.flip(sample)
        # clipped_data = np.flip(clipped_data)
        # improve p0
        p0 = p1
        # fit clipped with new p0
        p1, success = optimize.leastsq(errfunc, p0[:], args=(t, clipped_data))

        ## TOE PROCESS
        raw_impacts = np.subtract(sample, fitfunc(p1, t))
        raw_impacts = abs(raw_impacts)
        impacts_index = degfunc(p1, t)
        impacts_sum = np.zeros(360)

        for i in range(len(raw_impacts)):
            deg_index = int(np.around(impacts_index[i]))
            if deg_index == 360:  # correction for 360 to 0
                deg_index = 0
            impacts_sum[deg_index] += raw_impacts[i]
        # print impacts_sum
        impacts_angles = np.arange(toe_window_min, toe_window_max)
        try:
            mu = np.average(impacts_angles, weights=impacts_sum[toe_window_min:toe_window_max])
            std = math.sqrt(np.average((impacts_angles - mu) ** 2, weights=impacts_sum[toe_window_min:toe_window_max]))
            toe_in_degrees = mu
            toe_in_radians = mu * np.pi / 180
        except:
            pass

        ###
        # impacts = np.subtract(sample,fitfunc(p1,t))
        # impacts = abs(impacts)
        impacts.append(sum(abs(num) >= 12 for num in sample))

        hist, bin_edges = np.histogram(abs(np.array(sample)), bins=np.arange(4, 16, 0.4))
        hist2d.append(hist)

        RPM = abs(60 * (p1[1]))
        if (RPM > 9 and RPM < 11):
            speeds.append(RPM)
            toe.append(toe_in_degrees)
            toe_std.append(std)
            hist, bin_edges = np.histogram(sample, bins=np.arange(4, 16, 0.4))
            hist2d.append(hist)

        else:
            try:
                toe.append(toe[-1])
                toe_std.append(toe_std[-1])
                speeds.append(speeds[-1])
                hist2d.append(hist2d[-1])

            except:
                toe.append(180)
                toe_std.append(60)
                speeds.append(10)
                hist2d.append(np.zeros(len(np.arange(4, 16, 0.4))))

    hist2d = np.array(hist2d)  # conversion
    hist2d = np.flip(hist2d.T, 0)  # transpose and flip UD
    interval = [min(dates), max(dates)]

    return (speeds, hist2d, interval, p1, impacts, dates, toe, toe_std)


# plt.plot(sample)
# plt.plot(clipped_data)
# plt.plot(filtered_data)
# plt.plot(fitfunc(p1,t))
# plt.show
# plt.pause(5)
# plt.clf()


# Open database connection
db = MySQLdb.connect("hstech.sinc.cl", "jsanhueza", "Hstech2018.-)", "ssi_mlp_sag2")
cursor = db.cursor()

cursor.execute("SELECT dataZ , fecha_reg \
	FROM Data_Sensor \
	WHERE (id_sensor_data IN (3) AND estado_data = 134217726 \
	AND (fecha_reg BETWEEN %s AND %s) ) \
	ORDER BY fecha_reg ASC \
	LIMIT 5000", (startDate, endDate))

results = cursor.fetchall()
center_ring = process(results)

# print sample

# plt.ylim(0,14)
# plt.plot(speeds)
# plt.show()

# disconnect from server
# print dates
db.close()

# plt.set_yticklabels(dates)
# plt.imshow(hist2d, cmap='hot' , interpolation='none', aspect = 'auto', extent=[0,500,4,16])
# plt.show()
# plt.pause(15)


## Analysis completed, Show results


###  Lets lie a little

# toe = 0.660*np.pi
# shoulder = 1.68*np.pi

###
# pa = [1,1,1,1]

# p1 = p1 * pa

fig = plt.figure(figsize=(16, 9))
grid = plt.GridSpec(2, 3, wspace=0.2, hspace=0.5)
fig.suptitle("SSI Analyzer", fontsize=22)
fig.subplots_adjust(right=0.95, left=0.05)
fig.subplots_adjust(hspace=0.8)
fig.autofmt_xdate()

ax1 = fig.add_subplot(2, 3, 1)
ax1.set_title("Mill Speed")
ax1.grid(True)
ax1.set_ylim([0, 12])
ax1.plot(center_ring[5], center_ring[0], 'r')
date_format = mdates.DateFormatter('%d-%m %H:%M')
ax1.xaxis.set_major_formatter(date_format)
plt.xticks(rotation=-90)

ax2 = fig.add_subplot(grid[1, :2])  # 2,3,4)
ax2.set_title("Toe Angle")
ax2.grid(True)
x_lims = center_ring[2]
x_lims = mdates.date2num(x_lims)
ax2.set_ylim([100, 150])
# ax2.xaxis.set_major_formatter(mdates.DateFormatter('%Y-%m-%d'))
plt.xticks(rotation=-90)
# ax2.imshow(feeding_ring[1], cmap='hot' , interpolation='none', aspect = 'auto', extent=[x_lims[0],x_lims[1],4,16])
ax2.plot(center_ring[5], center_ring[6], 'r.')
ax2.plot(center_ring[5], signal.medfilt(center_ring[6], 27), 'k-', linewidth=3)
ax2.xaxis_date()
date_format = mdates.DateFormatter('%d-%m %H:%M')
ax2.xaxis.set_major_formatter(date_format)

# ax3 = fig.add_subplot(2,3,3)
# ax3.set_title("Impactos")
# ax3.grid(True)
# ax3.plot(degfunc(feeding_ring[3],t),feeding_ring[4],'b')
# ax3.hist2d(degfunc(p1,t),impacts)
# ax3.plot(t,np.cumsum(data))


if center_ring[3][0] < 0:
    center_ring[3][2] = center_ring[3][2] + np.pi

ax4 = fig.add_subplot(2, 3, 3, polar=True)
ax4.set_title("Molino SAG2")
ax4.set_theta_zero_location('N')
ax4.set_theta_direction(1)  ## Clockwise - Counter-clockWise
ax4.set_yticklabels([])
ax4.grid(True)
# ax4.plot(anglefunc(feeding_ring[3],t),16 - feeding_ring[4],'r')
# ax4.plot(np.linspace(1.99,5.27,num=100),np.full(100, 8),'g', alpha=0.5 )
# ax4.fill_between(np.linspace(toe,shoulder,num=100),0,np.full(100, 16),facecolor='green',alpha=0.5)
# ax4.annotate('Toe',xy=(toe,16),
#		xytext=(0.45,0.1),
#		textcoords='figure fraction',
#		arrowprops=dict(facecolor='black', shrink=0.05),
#		)


# ax5 = fig.add_subplot(2,3,5)
# ax5.set_title("Impacts Histogram")
# x_lims = center_ring[2]
# x_lims = mdates.date2num(x_lims)
# ax2.xaxis.set_major_formatter(mdates.DateFormatter('%Y-%m-%d'))
# plt.xticks(rotation=-90)
# ax5.imshow(center_ring[1], cmap='viridis' , interpolation='none', aspect = 'auto', extent=[x_lims[0],x_lims[1],4,16])
# ax5.xaxis_date()
# date_format = mdates.DateFormatter('%d-%m %H:%M')
# ax5.xaxis.set_major_formatter(date_format)


ax6 = fig.add_subplot(2, 3, 6)
ax6.set_title("Toe Angle STD")
ax6.grid(True)
x_lims = center_ring[2]
ax6.set_ylim([0, 50])
x_lims = mdates.date2num(x_lims)
# ax2.xaxis.set_major_formatter(mdates.DateFormatter('%Y-%m-%d'))
plt.xticks(rotation=-90)
ax6.plot(center_ring[5], center_ring[7], 'b')
date_format = mdates.DateFormatter('%d-%m %H:%M')
ax6.xaxis.set_major_formatter(date_format)

ax7 = fig.add_subplot(2, 3, 2)
ax7.set_title("Impacts above 12[G]")
ax7.grid(True)
ax7.plot(center_ring[5], center_ring[4], 'r')
date_format = mdates.DateFormatter('%d-%m %H:%M')
ax7.xaxis.set_major_formatter(date_format)
plt.xticks(rotation=-90)

plt.show()
