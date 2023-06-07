import { Injectable } from '@nestjs/common';
import { InfluxService } from '../influx/influx.service';
import { Point } from '@influxdata/influxdb-client';
import { addHours, parse } from 'date-and-time';

@Injectable()
export class EarthquakeService {
  constructor(private readonly influxService: InfluxService) {}

  async createEarthquake(
    Epicenter: string,
    MagnitudeValue: number,
    OriginTime: string,
  ): Promise<void> {
    const RegulerTime = parse(
      `${OriginTime} GMT+0800`,
      'YYYY-MM-DD HH:mm:ss [GMT]Z',
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
