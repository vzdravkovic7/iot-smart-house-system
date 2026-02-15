import { Component, OnInit } from '@angular/core';
import { StateService } from '../../services/state.service';
import { CommonModule } from '@angular/common';
import { FormsModule } from '@angular/forms';

interface DeviceState {
  value: number | string;
  measurement: string;
  runs_on: string;
  simulated: boolean;
  timestamp: string;
}

@Component({
  selector: 'app-dashboard',
  standalone: true,
  imports: [CommonModule, FormsModule],
  templateUrl: './dashboard.component.html',
  styleUrls: ['./dashboard.component.css']
})
export class DashboardComponent implements OnInit {

  state: Record<string, DeviceState> = {};
  loading = true;
  error = false;
  ALARM = false;
  system_armed = false;
  stopwatch = '';
  mode = '';

  constructor(private stateService: StateService) { }

  ngOnInit(): void {
    this.loadState();
    setInterval(() => this.loadState(), 2000);
  }

  loadState() {
    this.stateService.getAllState().subscribe({
      next: (data) => {
        console.log("dejta", data)
        this.ALARM = data["ALARM"]["value"]
        this.system_armed = data["system_armed"]["value"]
        this.state = data;
        this.loading = false;
      },
      error: (_) => {
        this.error = true;
        this.loading = false;
      }
    });
  }

  switchSystemArmed() {
    this.stateService.switchSystemArmed().subscribe({
      next: () => {
        this.system_armed = !this.system_armed;
      }
    })
  }

  switchAlarm() {
    this.stateService.switchAlarm().subscribe({
      next: () => {
        this.ALARM = !this.ALARM;
      }
    })
  }

  updateStopwatch() {
    this.stateService.updateStopwatch(this.stopwatch).subscribe({
      next: () => { }
    })
  }

  updateBRGB() {
    this.stateService.updateBRGB(this.mode).subscribe({
      next: () => { }
    })
  }
}
