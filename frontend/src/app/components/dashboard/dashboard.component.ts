import { Component, OnInit } from '@angular/core';
import { StateService } from '../../services/state.service';
import { CommonModule } from '@angular/common';

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
  imports: [CommonModule],
  templateUrl: './dashboard.component.html',
  styleUrls: ['./dashboard.component.css']
})
export class DashboardComponent implements OnInit {

  state: Record<string, DeviceState> = {};
  loading = true;
  error = false;

  constructor(private stateService: StateService) { }

  ngOnInit(): void {
    this.loadState();
    setInterval(() => this.loadState(), 2000);
  }

  loadState() {
    this.stateService.getAllState().subscribe({
      next: (data) => {
        console.log("dejta", data)
        this.state = data;
        this.loading = false;
      },
      error: (_) => {
        this.error = true;
        this.loading = false;
      }
    });
  }
}
