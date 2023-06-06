import { Injectable } from '@nestjs/common';
import { Earthquake } from './entites/earthquake.entity';
import { InfluxDB } from 'influx';
import { InfluxService } from '../influx/influx.service';
import { Point } from '@influxdata/influxdb-client';

@Injectable()
export class EarthquakeService {
  constructor(private readonly influxService: InfluxService) {}

  async createEarthquake(
    Epicenter: string,
    MagnitudeValue: number,
    OriginTime: Date,
  ): Promise<void> {
    const point = new Point('earthquake')
      .tag('Epicenter', Epicenter)
      .floatField('MagnitudeValue', MagnitudeValue)
      .timestamp(OriginTime);

    await this.influxService.writeRecord(
      point,
    );

    return;
  }
}
