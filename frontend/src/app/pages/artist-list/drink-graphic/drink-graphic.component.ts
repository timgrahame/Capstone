import { Component, OnInit, Input } from '@angular/core';
import { artist } from 'src/app/services/artists.service';

@Component({
  selector: 'app-artist-graphic',
  templateUrl: './artist-graphic.component.html',
  styleUrls: ['./artist-graphic.component.scss'],
})
export class artistGraphicComponent implements OnInit {
  @Input() artist: artist;

  constructor() { }

  ngOnInit() {}

}
