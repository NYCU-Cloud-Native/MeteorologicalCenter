import { Injectable } from '@nestjs/common';
import { InfluxService } from '../influx/influx.service';
import { Point } from '@influxdata/influxdb-client';

@Injectable()
export class EarthquakeService {
  constructor(private readonly influxService: InfluxService) {}

  async createEarthquake(
    Epicenter: string,
    MagnitudeValue: number,
    OriginTime: string,
  ): Promise<void> {
    const [date, times] = OriginTime.split(' ');
    const [year, month, day] = date.split('-');
    const [hour, min, sec] = times.split(':');
    const d = new Date();
    d.toUTCString();
    const RegulerTime = new Date(
      new Date(+year, +month - 1, +day, +hour, +min, +sec).toUTCString(),
    );
    console.log(RegulerTime);

    const point = new Point('earthquake')
      .tag('Epicenter', Epicenter)
      .floatField('MagnitudeValue', MagnitudeValue)
      .timestamp(RegulerTime);

    await this.influxService.writeRecord(point);

    return;
  }
}
