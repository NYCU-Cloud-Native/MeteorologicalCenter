import { Injectable } from '@nestjs/common';
import { Repository } from 'typeorm';
import { Earthquake } from './entites/earthquake.entity';
import { InfluxDB } from 'influx';
import { InfluxService } from 'src/influx/influx.service';
import { Point } from '@influxdata/influxdb-client';
import { IPoint } from 'influx';

@Injectable()
export class EarthquakeService {
    constructor( private readonly influxService: InfluxService){};

    async createEarthquake(
        Epicenter: string, 
        MagnitudeValue: number, 
        // AffectTainanFactory: boolean,
        // TainanIntensity: number,
        // AffectHsinchuFactory: boolean,
        // HsinchuIntensity: number,
        // AffectTaichungFactory: boolean,
        // TaichungIntensity: number, 
): Promise<void>{

    const mearsurement=process.env.INFLUX_MEARSUREMENT;

    const point = new Point('earthquake_measurement')
    .tag('Epicenter', Epicenter)
    .floatField('MagnitudeValue', MagnitudeValue);
    // .booleanField('AffectTainanFactory', AffectTainanFactory)
    // .floatField('TainanIntensity', TainanIntensity)
    // .booleanField('AffectHsinchuFactory', AffectHsinchuFactory)
    // .floatField('HsinchuIntensity', HsinchuIntensity)
    // .booleanField('AffectTaichungFactory', AffectTaichungFactory)
    // .floatField('TaichungIntensity', TaichungIntensity);
        
    
    const writeApi = await this.influxService.writeRecord(process.env.INFLUX_URL,point);

    return;
}
}
