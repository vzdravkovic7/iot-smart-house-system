import { Injectable } from '@angular/core';
import { HttpClient } from '@angular/common/http';
import { Observable } from 'rxjs';

@Injectable({
    providedIn: 'root'
})
export class StateService {

    private apiUrl = 'http://localhost:5000/api';

    constructor(private http: HttpClient) { }

    getAllState(): Observable<any> {
        return this.http.get(`${this.apiUrl}/state`);
    }

    getDeviceState(name: string): Observable<any> {
        return this.http.get(`${this.apiUrl}/state/${name}`);
    }
}
