import { Component, OnInit } from '@angular/core';
import { artistsService, artist } from '../../services/artists.service';
import { ModalController } from '@ionic/angular';
import { artistFormComponent } from './artist-form/artist-form.component';
import { AuthService } from 'src/app/services/auth.service';

@Component({
  selector: 'app-artist-menu',
  templateUrl: './artist-menu.page.html',
  styleUrls: ['./artist-menu.page.scss'],
})
export class artistMenuPage implements OnInit {
  Object = Object;

  constructor(
    private auth: AuthService,
    private modalCtrl: ModalController,
    public artists: artistsService
    ) { }

  ngOnInit() {
    this.artists.getartists();
  }

  async openForm(activeartist: artist = null) {
    if (!this.auth.can('get:artists-detail')) {
      return;
    }

    const modal = await this.modalCtrl.create({
      component: artistFormComponent,
      componentProps: { artist: activeartist, isNew: !activeartist }
    });

    modal.present();
  }

}
