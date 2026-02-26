import { Component, OnInit, OnDestroy } from '@angular/core';
import { StateService } from '../../services/state.service';
import { CommonModule } from '@angular/common';
import { FormsModule } from '@angular/forms';
import { Subscription, interval } from 'rxjs';
import { switchMap } from 'rxjs/operators';

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
export class DashboardComponent implements OnInit, OnDestroy {

  state: Record<string, DeviceState> = {};
  loading = true;
  error = false;
  ALARM = false;
  system_armed = false;
  stopwatch = '';
  mode = '';

  private pollingSubscription?: Subscription;

  constructor(private stateService: StateService) { }

  ngOnInit(): void {
    this.loadState();
    // Koristi RxJS interval umesto setInterval za bolju memory cleanup
    this.pollingSubscription = interval(2000)
      .pipe(switchMap(() => this.stateService.getAllState()))
      .subscribe({
        next: (data) => this.handleStateUpdate(data),
        error: () => {
          this.error = true;
          this.loading = false;
        }
      });
  }

  ngOnDestroy(): void {
    this.pollingSubscription?.unsubscribe();
  }

  loadState() {
    this.stateService.getAllState().subscribe({
      next: (data) => this.handleStateUpdate(data),
      error: () => {
        this.error = true;
        this.loading = false;
      }
    });
  }

  private handleStateUpdate(data: Record<string, DeviceState>) {
    this.ALARM = Boolean(data["ALARM"]["value"]);
    this.system_armed = Boolean(data["system_armed"]["value"]);
    this.state = data;
    this.loading = false;
    this.error = false;
  }

  switchSystemArmed() {
    this.stateService.switchSystemArmed().subscribe({
      next: () => {
        this.system_armed = !this.system_armed;
      },
      error: (err) => console.error('Error switching system armed:', err)
    });
  }

  switchAlarm() {
    this.stateService.switchAlarm().subscribe({
      next: () => {
        this.ALARM = !this.ALARM;
      },
      error: (err) => console.error('Error switching alarm:', err)
    });
  }

  updateStopwatch() {
    if (!this.stopwatch) {
      alert('Please enter a time value');
      return;
    }
    this.stateService.updateStopwatch(this.stopwatch).subscribe({
      next: () => {
        alert(`Timer set to ${this.stopwatch} seconds`);
        this.stopwatch = '';
      },
      error: (err) => console.error('Error updating stopwatch:', err)
    });
  }

  updateBRGB() {
    if (!this.mode) {
      alert('Please enter a mode value (0-7)');
      return;
    }
    this.stateService.updateBRGB(this.mode).subscribe({
      next: () => {
        alert(`RGB mode changed to ${this.mode}`);
        this.mode = '';
      },
      error: (err) => console.error('Error updating BRGB:', err)
    });
  }

  // Helper metode za formatiranje
  formatDeviceName(key: string): string {
    return key.replace(/_/g, ' ').toUpperCase();
  }

  formatValue(value: number | string, measurement: string): string {
    if (typeof value === 'boolean') {
      return value ? 'ON' : 'OFF';
    }
    if (measurement === 'temperature') {
      return `${value}°C`;
    }
    if (measurement === 'humidity') {
      return `${value}%`;
    }
    if (measurement === 'distance') {
      return `${value} cm`;
    }
    return String(value);
  }

  formatTimestamp(timestamp: string): string {
    try {
      const date = new Date(timestamp);
      return date.toLocaleTimeString('sr-RS', {
        hour: '2-digit',
        minute: '2-digit',
        second: '2-digit'
      });
    } catch {
      return timestamp;
    }
  }
}