import {
  Entity,
  Column,
  PrimaryGeneratedColumn,
  CreateDateColumn,
} from 'typeorm';

@Entity()
export class Earthquake {
  @PrimaryGeneratedColumn()
  id: number;

  @Column('Epicenter')
  epicCenter: string;

  @Column('MagnitudeValue')
  MagnitudeValue: number;

  @Column('AffectTainanFactory')
  Affect_SouthFactory: boolean;

  @Column('TainanIntensity')
  TainanIntensity: number;

  @Column('AffectHsinchuFactory')
  Affect_HsinchuFactory: boolean;

  @Column('HsinchuIntensity')
  Intensity: number;

  @Column('AffectTaichungFactory')
  Affect_TaichungFactory: boolean;

  @Column('TaichungIntensity')
  TaichungIntensity: number;

  @CreateDateColumn()
  createdAt: Date;
}
