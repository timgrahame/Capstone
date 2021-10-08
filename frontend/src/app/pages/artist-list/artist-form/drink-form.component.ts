import { Component, OnInit, Input } from '@angular/core';
import { artist, artistsService } from 'src/app/services/artists.service';
import { ModalController } from '@ionic/angular';
import { AuthService } from 'src/app/services/auth.service';

@Component({
  selector: 'app-artist-form',
  templateUrl: './artist-form.component.html',
  styleUrls: ['./artist-form.component.scss'],
})
export class artistFormComponent implements OnInit {
  @Input() artist: artist;
  @Input() isNew: boolean;

  constructor(
    public auth: AuthService,
    private modalCtrl: ModalController,
    private artistService: artistsService
    ) { }

  ngOnInit() {
    if (this.isNew) {
      this.artist = {
        id: -1,
        title: '',
        recipe: []
      };
      this.addIngredient();
    }
  }

  customTrackBy(index: number, obj: any): any {
    return index;
  }

  addIngredient(i: number = 0) {
    this.artist.recipe.splice(i + 1, 0, {name: '', color: 'white', parts: 1});
  }

  removeIngredient(i: number) {
    this.artist.recipe.splice(i, 1);
  }

  closeModal() {
    this.modalCtrl.dismiss();
  }

  saveClicked() {
    this.artistService.saveartist(this.artist);
    this.closeModal();
  }

  deleteClicked() {
    this.artistService.deleteartist(this.artist);
    this.closeModal();
  }
}
